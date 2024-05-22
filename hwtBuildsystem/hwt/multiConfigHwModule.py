from copy import copy
from typing import List, Dict, Tuple, Union

from hdlConvertorAst.hdlAst import HdlIdDef, HdlValueId, HdlStmIf, \
    HdlStmBlock, HdlModuleDef, HdlCompInst
from hwt.code import And
from hwt.doc_markers import internal
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.types.defs import BIT, INT
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.const import HConst
from hwt.pyUtils.setList import SetList
from hwt.serializer.mode import hwParamsToValTuple
from hwt.synthesizer.dummyPlatform import DummyPlatform
from hwt.hObjList import HObjList
from hwt.hwParam import HwParam
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.hwModule import HwModule
from hwt.synth import synthesised
from ipCorePackager.constants import INTF_DIRECTION, DIRECTION


def reduce_ternary(cond_val_pairs: List[Tuple[Union[HConst, RtlSignal], Union[HConst, RtlSignal]]], default: Union[HConst, RtlSignal]):
    """
    .. code-block:: python

        reduce_ternary([(c0, v0), (c1, v1)], v3)
        # to
        v0 if c0 else v1 if c1 else v3
    """
    res = default
    for cond, val in reversed(cond_val_pairs):
        res = cond._ternary(val, res)

    return res


class MultiConfigHwModuleWrapper(HwModule):
    """
    Class which creates wrapper around multiple unit instances,
    the implementation is chosen based on generic/parameter values in HDL

    :attention: This is meant to be used for top component only, because it is useless
        for hwt design and it is useful only for integration of statically build
        component in to VHDL/Verilog
    """

    def __init__(self, possible_variants: List[HwModule]):
        assert possible_variants
        self._possible_variants = possible_variants
        super(MultiConfigHwModuleWrapper, self).__init__()

    def _copyParamsAndInterfaces(self):
        # note that the parameters are not added to HdlModuleDef (VHDL entity, Verilog module header)
        # as it was already build
        for p in self._possible_variants[0]._hwParams:
            myP = HwParam(p.get_value())
            self._registerParameter(p._name, myP)
            myP.set_value(p.get_value())

        ns = self._store_manager.name_scope
        for p in sorted(self._hwParams, key=lambda x: x._name):
            hdl_val = p.get_hdl_value()
            v = HdlIdDef()
            v.origin = p
            v.name = p._name = ns.checked_name(p._name, p)
            v.type = hdl_val._dtype
            v.value = hdl_val
            self._ctx.hwModDec.params.append(v)

        for hwIO in self.possible_variants[0]._hwIOs:
            # clone interface
            myHwIO = copy(hwIO)
            if hasattr(myHwIO, "_dtype"):
                myHwIO._dtype = copy(myHwIO._dtype)
            # sub-interfaces are not instantiated yet
            # myHwIO._direction = hwIO._direction
            myHwIO._direction = INTF_DIRECTION.opposite(hwIO._direction)

            self._registerHwIO(hwIO._name, myHwIO)
            object.__setattr__(self, hwIO._name, myHwIO)

        ei = self._ctx.hwIOs
        for hwIO in self._hwIOs:
            self._loadInterface(hwIO, True)
            assert hwIO._isExtern
            hwIO._signalsForHwIO(self._ctx, ei,
                                   self._store_manager.name_scope,
                                   reverse_dir=True)

    def _getDefaultName(self):
        return self._possible_variants[0]._getDefaultName()

    def _get_hdl_doc(self):
        return self._possible_variants[0]._get_hdl_doc()

    def _checkCompInstances(self):
        pass

    def _collectPortTypeVariants(self) -> List[Tuple[HdlPortItem, Dict[Tuple[HwParam, HConst], List[HdlType]]]]:
        res = []
        param_variants = [hwParamsToValTuple(subMod) for subMod in self._subHwModules]
        for parent_port, port_variants in zip(self._ctx.hwModDec.ports, zip(*(subMod._ctx.hwModDec.ports for subMod in self._subHwModules))):
            param_val_to_t = {}
            for port_variant, params in zip(port_variants, param_variants):
                assert port_variant.name == parent_port.name, (port_variant.name, parent_port.name)
                t = port_variant._dtype
                assert len(params) == len(self._hwParams), (params, self._hwParams)
                params = params._asdict()
                for p in self._hwParams:
                    p_val = params[p._name]
                    types = param_val_to_t.setdefault((p, p_val), SetList())
                    types.append(t)

            res.append((parent_port, param_val_to_t))

        return res

    def _injectParametersIntoPortTypes(self,
                                       port_type_variants: List[Tuple[HdlPortItem, Dict[Tuple[HwParam, HConst], List[HdlType]]]],
                                       param_signals: List[RtlSignal]):
        updated_type_ids = set()
        param_sig_by_name = {p._name: p for p in param_signals}
        param_value_domain = {}
        for parent_port, param_val_to_t in port_type_variants:
            for (param, param_value), port_types in param_val_to_t.items():
                param_value_domain.setdefault(param, set()).add(param_value)

        for parent_port, param_val_to_t in port_type_variants:
            if id(parent_port._dtype) in updated_type_ids:
                continue
            # check which unique parameter values affects the type of the port
            # if the type changes with any parameter value integrate it in to type of the port
            # print(parent_port, param_val_to_t)
            type_to_param_values = {}
            for (param, param_value), port_types in param_val_to_t.items():
                for pt in port_types:
                    cond = type_to_param_values.setdefault(pt, SetList())
                    cond.append((param, param_value))

            assert type_to_param_values, parent_port
            if len(type_to_param_values) == 1:
                continue  # type does not change

            # HwParam: values
            params_used = {}
            for t, param_values in type_to_param_values.items():
                for (param, param_val) in param_values:
                    params_used.setdefault(param, set()).add(param_val)

                # filter out parameters which are not part of type specification process
                for p, p_vals in list(params_used.items()):
                    if len(param_value_domain[p]) == len(p_vals):
                        params_used.pop(p)
                # reset sets used to check parameter values
                for p, p_vals in params_used.items():
                    p_vals.clear()

            if not params_used:
                raise AssertionError(parent_port, "Type changes between the variants but it does not depend on parameter", param_val_to_t)

            if len(params_used) == 1 and list(params_used.keys())[0].get_hdl_type() == INT:
                # try to extract param * x + y
                p_val_to_port_w = {}
                for t, param_values in type_to_param_values.items():
                    for (param, param_val) in param_values:
                        if param not in params_used:
                            continue
                        assert param_val not in p_val_to_port_w or p_val_to_port_w[param_val] == t.bit_length(), parent_port
                        p_val_to_port_w[param_val] = t.bit_length()
                # t_width = n*p + c
                _p_val_to_port_w = sorted(p_val_to_port_w.items())
                t_width0, p0 = _p_val_to_port_w[0]
                t_width1, p1 = _p_val_to_port_w[1]
                # 0 == t_width0 - n*p0 + c
                # 0 == t_width1 - n*p1 + c

                # 0 == t_width0 - n*p0 - c + t_width1 - n*p1 - c
                # 0 == t_width0 + t_width1 - n*(p0 + p1) - 2c
                # c == (t_width0 + t_width1 - n*(p0 + p1) ) //2
                # n has to be int, 0 < n <= t_width0/p0
                # n is something like base size of port which is multiplied by parameter
                # we searching n for which we can resolve c
                found_nc = None
                for n in range(1, t_width0 // p0 + 1):
                    c = (t_width0 + t_width1 - n * (p0 + p1)) // 2
                    if t_width0 - n * p0 + c == 0 and t_width1 - n * p1 + c == 0:
                        found_nc = (n, c)
                        break

                if found_nc is None:
                    raise NotImplementedError()
                else:
                    p = list(params_used.keys())[0]
                    p = param_sig_by_name[p._name]
                    (n, c) = found_nc
                    t = parent_port._dtype
                    t._bit_length = INT.from_py(n) * p + c
                    t._bit_length._const = True
                    updated_type_ids.add(id(t))
            else:
                condition_and_type_width = []
                default_width = None
                for t, p_vals in sorted(type_to_param_values.items(), key=lambda x: x[0].bit_length()):
                    cond = And(
                        *(param_sig_by_name[p._name]._eq(p_val)
                        for p, p_val in p_vals if p in params_used)
                    )
                    w = t.bit_length()
                    if default_width is None:
                        default_width = w
                    condition_and_type_width.append((cond, w))

                t = parent_port._dtype
                t._bit_length = reduce_ternary(condition_and_type_width, default_width)
                t._bit_length._const = True
                updated_type_ids.add(id(t))

    def create_HdlModuleDef(self,
                            target_platform: DummyPlatform,
                            store_manager: "StoreManager"):
        ctx = self._ctx
        mdef = HdlModuleDef()
        mdef.dec = ctx.hwModDec
        mdef.module_name = HdlValueId(ctx.hwModDec.name, obj=ctx.hwModDec)
        mdef.name = "rtl"

        # constant signals which represents the param/generic values
        param_signals = [
            ctx.sig(p._name, p.get_hdl_type(), def_val=p.get_hdl_value())
            for p in sorted(self._hwParams, key=lambda x: x._name)
        ]
        # rewrite ports to use generic/params of this entity/module
        port_type_variants = self._collectPortTypeVariants()
        self._injectParametersIntoPortTypes(port_type_variants, param_signals)
        for p in param_signals:
            p._const = True
            p.hidden = False
        # instantiate component variants in if generate statement
        ns = store_manager.name_scope
        as_hdl_ast = self._store_manager.as_hdl_ast
        if_generate_cases = []
        for subMod in self._subHwModules:
            # create instance
            ci = HdlCompInst()
            ci.origin = subMod
            ci.module_name = HdlValueId(subMod._ctx.hwModDec.name, obj=subMod._ctx.hwModDec)
            ci.name = HdlValueId(ns.checked_name(subMod._name + "_inst", ci), obj=subMod)
            e = subMod._ctx.hwModDec

            ci.param_map.extend(e.params)
            # connect ports
            assert len(e.ports) == len(ctx.hwModDec.ports)
            for p, parent_port in zip(e.ports, ctx.hwModDec.ports):
                i = p.getInternSig()
                parent_port_sig = parent_port.getInternSig()
                assert i._name == parent_port_sig._name
                o = p.getOuterSig()

                # can not connect directly to parent port because type is different
                # but need to connect to something with the same name
                if o is p.src:
                    p.src = p.dst
                else:
                    assert o is p.dst, (o, p.dst)
                    p.dst = p.src

                ci.port_map.append(p)

            # create if generate instantiation condition
            param_cmp_expr = BIT.from_py(1)
            assert len(subMod._hwParams) == len(param_signals)
            for p, p_sig in zip(sorted(subMod._hwParams, key=lambda x: x._name), param_signals):
                assert p._name == p_sig._name, (p._name, p_sig._name)
                param_cmp_expr = param_cmp_expr & p_sig._eq(p.get_hdl_value())

            # add case if generate statement
            _param_cmp_expr = as_hdl_ast.as_hdl(param_cmp_expr)
            ci = as_hdl_ast.as_hdl_HdlCompInst(ci)
            b = HdlStmBlock()
            b.body.append(ci)
            b.in_preproc = True
            if_generate_cases.append((_param_cmp_expr, b))

        if_generate = HdlStmIf()
        if_generate.in_preproc = True
        if_generate.labels.append(ns.checked_name("implementation_select", if_generate))
        for c, ci in if_generate_cases:
            if if_generate.cond is None:
                if_generate.cond = c
                if_generate.if_true = ci
            else:
                if_generate.elifs.append((c, ci))
        if_generate.if_false = store_manager.as_hdl_ast._static_assert_false(
            "The component was generated for this generic/params combination")

        mdef.objs.append(if_generate)
        for p in ctx.hwModDec.ports:
            s = p.getInternSig()
            if p.direction != DIRECTION.IN:
                s.drivers.append(if_generate)
            else:
                s.endpoints.append(if_generate)

        ctx.hwModDef = mdef
        return mdef

    @internal
    def _to_rtl(self, target_platform:DummyPlatform,
        store_manager:"StoreManager", add_param_asserts=False):
        return HwModule._to_rtl(self, target_platform, store_manager, add_param_asserts=add_param_asserts)

    def _impl(self):
        assert self._parent is None, "should be used only for top instances"
        self._ctx.create_HdlModuleDef = self.create_HdlModuleDef
        self.possible_variants = HObjList(self._possible_variants)
        self._copyParamsAndInterfaces()


if __name__ == "__main__":
    from hwtLib.examples.axi.simpleAxiRegs import SimpleAxiRegs
    from hwt.synth import to_rtl_str

    variants = []
    for aw in [8, 16, 32]:
        m = SimpleAxiRegs()
        m.ADDR_WIDTH = aw
        m.DATA_WIDTH = 32
        variants.append(m)

    m = MultiConfigHwModuleWrapper(variants)
    # synthesised(m)
    print(to_rtl_str(m))
    #print(m._hwParams)


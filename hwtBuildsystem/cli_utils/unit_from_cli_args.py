
import argparse
import inspect
from io import StringIO
import os
import sys
from typing import Type, Optional, List, Dict

from hwt.serializer.store_manager import SaveToSingleFiles
from hwt.serializer.verilog import VerilogSerializer
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl
from hwtBuildsystem.hwt.multiConfigUnit import MultiConfigUnitWrapper
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword


def _parse_configs(defInstance: Unit, args: List[str], default_params: List[Dict[str, object]]):
    configs_cnt = None
    for p in defInstance._params:
        v = getattr(args, p._name)
        if configs_cnt is None:
            configs_cnt = len(v)
        else:
            assert configs_cnt == len(v), ("All paramenters must have same number of values,"
                                           " because each item represents a value for specific combination")
    assert configs_cnt is not None, ("At least some parameters needs to be specified,"
        " otherwise you can instanciate component directly and you do not need this function")

    unitConfigs = []
    for i in range(configs_cnt):
        conf = {}
        for p in defInstance._params:
            v = getattr(args, p._name)
            v = p.get_value().__class__(v[i])
            conf[p._name] = v
        unitConfigs.append(conf)

    for conf in default_params:
        assert len(conf) == len(defInstance._params), (conf, defInstance._params)
        for p in defInstance._params:
            v = conf[p._name]
            v = p.get_value().__class__(v)
            conf[p._name] = v

        unitConfigs.append(conf)

    unitConfigs = [tuple(sorted(c.items(), key=lambda x: x[0])) for c in unitConfigs]
    seenConfigs = set()
    for c in unitConfigs:
        if c not in seenConfigs:
            yield c
            seenConfigs.add(c)


def ban_names_in_serializer(serializer_cls: Type, reserved_ids: Optional[List[str]]) -> Type:
    if reserved_ids is None:
        return serializer_cls
    else:

        class ToHdlAst(serializer_cls.TO_HDL_AST):
            _keywords_dict = dict(serializer_cls.TO_HDL_AST._keywords_dict,
                                  **{name: LanguageKeyword() for name in reserved_ids})

        class Serializer(serializer_cls):
            TO_HDL_AST = ToHdlAst

        return Serializer


def unit_from_cli_args(unitCls: Type,
                       default_params: List[Dict[str, object]],
                       args:Optional[List[str]]=None,
                       out_folder:Optional[str]=None,
                       unit_name:Optional[str]=None,
                       reserved_ids:Optional[List[str]]=None,
                       stdout:StringIO=None):
    """
    :param unitCls: unit class or anything callable which produces instance of Unit
    :param default_params: list of default parameters for a component to resolve which parameters/generics affect which port width
    :param args: list of CLI arguments, if None the CLI args of this python execution are used
    :param reserved_ids: optional list of identifier names which should not be used in generated code (used to prevent name collisions)
    """
    defInstance = unitCls()
    if stdout is None:
        stdout = sys.stdout

    parser = argparse.ArgumentParser('Generate hwt component files from specification of possible parameter/generic values')
    parser.add_argument('-f', '--files', action='store_true', help='Print all source absolute file paths')
    parser.add_argument('-g', '--generics', action='store_true', help='Print component generics')
    parser.add_argument('-c', '--component', action='store_true', help='Print component name')
    parser.add_argument('-l', '--language', type=str, choices=["vhdl2008", "sv2012"], default="vhdl2008", help='Specifies target language')
    for p in defInstance._params:
        parser.add_argument(f'--{p._name}', default=[p.get_value(), ], nargs='+')

    args = parser.parse_args(args=args)

    if args.component:
        stdout.write(str(defInstance._getDefaultName()))
        return

    if args.generics:
        stdout.write(str(' '.join([p._name for p in defInstance._params])))
        return

    unitVariants = []
    for conf in _parse_configs(defInstance, args, default_params):
        curInst = unitCls()
        for param_name, param_value in conf:
            setattr(curInst, param_name, param_value)

        unitVariants.append(curInst)

    if unit_name is None:
        unitFile = inspect.getfile(defInstance.__class__)
        unit_name = os.path.splitext(os.path.basename(unitFile))[0]

    if out_folder is None:
        out_folder = os.getcwd()

    rtl_dir_path = os.path.join(out_folder,
                                unit_name)
    serializers = {
        "vhdl2008": ban_names_in_serializer(Vhdl2008Serializer, reserved_ids),
        "sv2012": ban_names_in_serializer(VerilogSerializer, reserved_ids),
    }
    store_man = SaveToSingleFiles(serializers[args.language], rtl_dir_path, name=unit_name)
    multiConfUnit = MultiConfigUnitWrapper(unitVariants)
    to_rtl(multiConfUnit, store_manager=store_man)

    if args.files:
        stdout.write(str(' '.join(list(filter(None, store_man.files)))))
        return

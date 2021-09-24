
import argparse
import inspect
import os
from typing import Type, Optional, List

from hwt.serializer.store_manager import SaveToSingleFiles
from hwt.serializer.vhdl import Vhdl2008Serializer as HwtVhdlSerializer
from hwt.synthesizer.utils import to_rtl
from hwtLib.examples.hierarchy.multiConfigUnit import MultiConfigUnitWrapper


def unit_from_cli_args(unitCls: Type, args:Optional[List[str]]=None):
    """
    :param unitCls: unit class or anything callable which produces instance of Unit
    :param args: list of CLI arguments, if None the CLI args of this python execution are used
    """

    # Todo: Addwrapper for multigeneric configuration
    defInstance = unitCls()
    defUnit = MultiConfigUnitWrapper([defInstance])

    unitFile = inspect.getfile(defInstance.__class__)
    compName = os.path.splitext(os.path.basename(unitFile))[0]
    rtl_dir_path = os.path.join(os.path.dirname(os.path.realpath(unitFile)),
                                compName)
    store_man = SaveToSingleFiles(HwtVhdlSerializer, rtl_dir_path, name=compName)

    param_unit = MultiConfigUnitWrapper([unitCls()])
    to_rtl(param_unit, store_manager=store_man)

    parser = argparse.ArgumentParser('Vivado integrator for hwt component')
    parser.add_argument('-f', '--files', action='store_true', help='Print all source absolute file paths')
    parser.add_argument('-g', '--generics', action='store_true', help='Print component generics')
    parser.add_argument('-c', '--component', action='store_true', help='Print component name')
    for p in param_unit._params:
        parser.add_argument(f'--{p._name}', default=p.get_value(), nargs='+')

    args = parser.parse_args(args=args)

    assert int(args.generics) + int(args.files) + int(args.component) == 1, ("Mus use exacly one cli option (--files/--generics/--componnet)")
    if(args.component == True):
        print(param_unit._getDefaultName())
        return

    unitConfigs = []
    has_next = True
    while has_next:
        has_next = False
        curIndex = len(unitConfigs)
        curInst = unitCls()
        for p in param_unit._params:
            v = getattr(args, p._name)
            if(len(v) > curIndex):
                p.set_value(v[curIndex])
            if(len(v) > curIndex + 1):
                has_next = True
        unitConfigs.append(curInst)

    multiConfUnit = MultiConfigUnitWrapper(unitConfigs)
    to_rtl(multiConfUnit, store_manager=store_man)

    if(args.generics == True):
        print(' '.join([p.hdl_name for p in defUnit._params]))
        return

    if(args.files == True):
        print(' '.join(list(filter(None, store_man.files))))
        return

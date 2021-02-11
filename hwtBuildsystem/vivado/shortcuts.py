import os

from hwt.serializer.store_manager import SaveToFilesFlat
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl
from hwtBuildsystem.vivado.api import FILE_TYPE
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from hwtBuildsystem.vivado.report import VivadoReport
from hwtBuildsystem.common.executor import ToolExecutor

__pb = XilinxPartBuilder
DEFAULT_PART = XilinxPartBuilder(
    __pb.Family.kintex7,
    __pb.Size._160t,
    __pb.Package.ffg676,
    __pb.Speedgrade._2).name()


def buildUnit(v: ToolExecutor, unit: Unit, root:str,
              synthesize=True, implement=True, writeBitstream=True,
              openGui=False, part=DEFAULT_PART) -> VivadoReport:
    """
    Synthetize unit in bitstream synthesis tool
    """

    def synthesizeCmds(p):
        # generate project
        if p._exists():
            p._remove()

        yield from p.create()
        yield from p.setPart(part)

        # generate files
        store_manager = SaveToFilesFlat(Vhdl2008Serializer, root=os.path.join(p.path, 'src'))
        to_rtl(unit, store_manager=store_manager)
        hdls = []
        xdcs = []
        for f in store_manager.files:
            if f.endswith(".xdc"):
                xdcs.append(f)
            else:
                hdls.append(f)

        yield from p.addDesignFiles(hdls)
        for f in hdls:
            if f.endswith(".vhd"):
                yield from p.setFileType(os.path.abspath(f), FILE_TYPE.VHDL_2008)

        yield from p.setTop(unit._name)
        if xdcs is not None:
            for xdc in xdcs:
                yield from p.addXdcFile(xdc)

        if synthesize:
            yield from p.synthAll()

        if implement:
            yield from p.implemAll()

        if writeBitstream:
            yield from p.writeBitstream()

    uName = unit._getDefaultName()
    p = v.project(root, uName)
    v.process(synthesizeCmds(p))
    if openGui:
        v.openGui()
    return p.report()

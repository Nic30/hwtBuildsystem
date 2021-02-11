import multiprocessing
import os

from hwt.serializer.store_manager import SaveToFilesFlat
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl
from hwtBuildsystem.vivado.api import FILE_TYPE
from hwtBuildsystem.vivado.api.project import Project
from hwtBuildsystem.vivado.controller import VivadoCntrl
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from hwtBuildsystem.vivado.report import VivadoReport

__pb = XilinxPartBuilder
DEFAULT_PART = XilinxPartBuilder(
    __pb.Family.kintex7,
    __pb.Size._160t,
    __pb.Package.ffg676,
    __pb.Speedgrade._2).name()


def buildUnit(unit: Unit, root:str,
              synthesize=True, implement=True, writeBitstream=True,
              log=True, openGui=False, part=DEFAULT_PART,
              workerCnt=multiprocessing.cpu_count()) -> VivadoReport:
    """
    Synthetize unit in bitstream synthesis tool
    """
    uName = unit._getDefaultName()
    p = Project(root, uName, workerCnt)
    r = VivadoReport(p.path, p.name, uName)

    def synthesizeCmds():
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
            r.setSynthFileNames()

        if implement:
            yield from p.implemAll()
            r.setImplFileNames()

        if writeBitstream:
            yield from p.writeBitstream()
            r.setBitstreamFileName()

    with VivadoCntrl(logComunication=log) as v:
        v.process(synthesizeCmds())
        if openGui:
            v.openGui()

    return r

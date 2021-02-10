import multiprocessing
import os

from hwt.serializer.store_manager import SaveToFilesFlat
from hwt.serializer.vhdl import Vhdl2008Serializer
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.utils import to_rtl
from hwtBuildsystem.vivado.api import FILE_TYPE
from hwtBuildsystem.vivado.api.project import Project
from hwtBuildsystem.vivado.config import VivadoConfig
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
    r = VivadoReport()
    uName = unit._getDefaultName()

    def synthesizeCmds(workerCnt):
        # generate project
        p = Project(root, uName, workerCnt)
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
            # collect report files
            r.utilizationSynth = os.path.join(
                p.path, p.name + ".runs",
                "synth_1", uName + "_utilization_synth.rpt")

        if implement:
            impl = os.path.join(p.path, p.name + ".runs", "impl_1")
            implP = lambda n: os.path.join(impl, uName + "_" + n + ".rpt")
            yield from p.implemAll()
            # collect report files
            r.dcrOpted = implP("drc_opted")
            r.ioPlaced = implP("io_placed")
            r.dcrRouted = implP("drc_routed")
            r.powerRouted = implP("power_routed")
            r.routeStatus = implP("route_status")
            r.utilizationPlaced = implP("utilization_placed")
            r.controlSetsPlaced = implP("control_sets_placed")
            r.timingSummaryRouted = implP("timing_summary_routed")
            r.clokUtilizationRouted = implP("clock_utilization_routed")

        if writeBitstream:
            yield from p.writeBitstream()
            r.bitstreamFile = os.path.join(impl, unit._name + ".bit")

    with VivadoCntrl(VivadoConfig.getExec(), logComunication=log) as v:
        v.process(synthesizeCmds(workerCnt))
        if openGui:
            v.openGui()

    return r

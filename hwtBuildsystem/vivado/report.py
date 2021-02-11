from hwtBuildsystem.vivado.logParser.synthesis import VivadoSynthesisLogParser
import os


class VivadoReport():
    """
    This class is output from hardware synthesis made by vivado
    All attributes are filenames
    """

    def __init__(self, projectRoot:str, projectName:str, topName:str):
        self.projectRoot = projectRoot
        self.projectName = projectName
        self.topName = topName
        # synth
        self.utilizationSynth = None
        # impl
        self.dcrOpted = None
        self.ioPlaced = None
        self.dcrRouted = None
        self.powerRouted = None
        self.routeStatus = None
        self.utilizationPlaced = None
        self.controlSetsPlaced = None
        self.timingSummaryRouted = None
        self.clokUtilizationRouted = None
        self.bitstreamFile = None

    def setSynthFileNames(self, runName="synth_1"):
        self.utilizationSynth = os.path.join(
                self.projectRoot, self.projectName + ".runs",
                runName, self.topName + "_utilization_synth.rpt")

    def setImplFileNames(self, runName="impl_1"):
        impl = os.path.join(self.projectRoot, self.projectName + ".runs", runName)
        implP = lambda n: os.path.join(impl, self.topName + "_" + n + ".rpt")
        # collect report files
        self.dcrOpted = implP("drc_opted")
        self.ioPlaced = implP("io_placed")
        self.dcrRouted = implP("drc_routed")
        self.powerRouted = implP("power_routed")
        self.routeStatus = implP("route_status")
        self.utilizationPlaced = implP("utilization_placed")
        self.controlSetsPlaced = implP("control_sets_placed")
        self.timingSummaryRouted = implP("timing_summary_routed")
        self.clokUtilizationRouted = implP("clock_utilization_routed")

    def setBitstreamFileName(self, runName="impl_1"):
        impl = os.path.join(self.projectRoot, self.projectName + ".runs", runName)
        self.bitstreamFile = os.path.join(impl, self.topName + ".bit")

    def parseUtilizationSynth(self):
        with open(self.utilizationSynth) as f:
            d = f.read()
        r = VivadoSynthesisLogParser(d)
        r.parse()
        return r

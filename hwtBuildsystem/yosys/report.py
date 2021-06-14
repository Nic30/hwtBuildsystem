from hwtBuildsystem.yosys.logParser.synthesis import YosysSynthesisLogParser


class YosysReport():
    """
    This class is output from hardware synthesis made by Intel Quartus
    """

    def __init__(self, projectRoot:str, projectName:str, topName:str):
        self.projectRoot = projectRoot
        self.projectName = projectName
        self.topName = topName
        self.utilizationSynth = None
        self.implLog = None
        self.bitstreamFile = None

    def setSynthLog(self, text:str):
        self.utilizationSynth = text

    def setImplLog(self, text:str):
        self.utilizationSynth = text

    def setBitstreamFileName(self):
        pass
        # impl = os.path.join(self.projectRoot, self.projectName + ".runs", runName)
        # self.bitstreamFile = os.path.join(impl, self.topName + ".bit")

    def parseUtilizationSynth(self):
        r = YosysSynthesisLogParser(self.utilizationSynth, self.topName)
        r.parse()
        return r

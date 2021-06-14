import os

from hwtBuildsystem.quartus.logParser.synthesis import QuartusSynthesisLogParser


class QuartusReport():
    """
    This class is output from hardware synthesis made by Intel Quartus
    """

    def __init__(self, projectRoot:str, projectName:str, topName:str):
        self.projectRoot = projectRoot
        self.projectName = projectName
        self.topName = topName
        # synth
        self.utilizationSynth = None
        self.bitstreamFile = None

    def setSynthFileNames(self):
        self.utilizationSynth = os.path.join(self.projectRoot, self.topName + ".map.rpt")

    def setImplFileNames(self):
        raise NotImplementedError()

    def setBitstreamFileName(self):
        raise NotImplementedError()

    def parseUtilizationSynth(self):
        with open(self.utilizationSynth) as f:
            d = f.read()
        r = QuartusSynthesisLogParser(d)
        r.parse()
        return r

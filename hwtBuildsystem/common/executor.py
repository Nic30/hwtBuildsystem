from typing import Optional

from hwtBuildsystem.common.project import SynthesisToolProject
from hwtBuildsystem.common.cmdResult import TclCmdResult


class ToolExecutor():
    """
    An abstract class for a tool executors.
    Tool executor is an object which controlls some external tool in real time on command-output basis.
    """

    def __init__(self, workerCnt:Optional[int]=None):
        """
        :param workerCnt: used to limit the number of worker threads
        """
        self.workerCnt = workerCnt

    def getVersion(self):
        raise NotImplementedError()

    def exeCmd(self, cmd) -> TclCmdResult:
        raise NotImplementedError("Should be implemented in concrete implementation of this class")

    def project(self, root, name:str) -> SynthesisToolProject:
        raise NotImplementedError()

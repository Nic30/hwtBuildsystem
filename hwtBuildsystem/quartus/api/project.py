import os
from pathlib import Path
from typing import Tuple

from hwtBuildsystem.common.project import SynthesisToolProject
from hwtBuildsystem.quartus.report import QuartusReport


class QuartusProject(SynthesisToolProject):
    """
    :attention: After project is opened the currend directory is changed to

    """

    SUFFIX_TO_FILE_TYPE = {
        ".v": "VERILOG_FILE",
        ".vhd": "VHDL_FILE",
        ".vh": "VERILOG_INCLUDE_FILE",
        ".svh": "VERILOG_INCLUDE_FILE",
        ".sv": "SYSTEMVERILOG_FILE",
        ".sdc": "SDC_FILE",
        ".ip": "IP_FILE",
    }

    def __init__(self, executor: "QuartusExecutor", path:str, name:str):
        super(QuartusProject, self).__init__(executor, path, name)
        self.name = name
        # j = os.path.join
        # self.projFile = j(path, name, name + ".xpr")

        self._report = QuartusReport(self.path, self.name, None)

    def _defaultTclImports(self):
        exe = self.executor.exeCmd
        exe(f'package require ::quartus::project')
        exe(f'package require ::quartus::flow')

    def setPart(self, part: Tuple[str, str]):
        """
        :param part: tuple family, part number e.g ("Cyclone", "EP1C12F256C6")
        """
        self.part = part
        family, device = part
        exe = self.executor.exeCmd
        exe(f'set_global_assignment -name FAMILY "{family:s}"')
        exe(f'set_global_assignment -name DEVICE {device:s}')

    def setTop(self, topName):
        self.top = topName
        self._report.topName = topName
        exe = self.executor.exeCmd
        exe(f'set_global_assignment -name TOP_LEVEL_ENTITY {self.top:s}')

    def create(self):
        # https://www.intel.com/content/www/us/en/programmable/documentation/jeb1529967983176.html#mwh1410471006061
        os.makedirs(self.path, exist_ok=True)
        exe = self.executor.exeCmd
        exe(f'cd "{self.path:s}"')
        exe(f'project_new {self.name:s} -overwrite')
        if self.executor.workerCnt is not None:
            exe(f"set_param general.maxThreads {self.workerCnt:d}")
        exe(f'project_open {self.name:s}')

    def addConstrainFiles(self, files):
        exe = self.executor.exeCmd
        for f in files:
            exe(f"set_global_assignment -name SDC_FILE '{f:s}'")

    def addDesignFiles(self, files):
        # https://www.intel.com/content/www/us/en/programmable/documentation/eca1490998903550.html#mnl1088
        exe = self.executor.exeCmd
        for f in files:
            suffix = os.path.splitext(f)[1].lower()
            t = self.SUFFIX_TO_FILE_TYPE[suffix]
            f = str(Path(f).relative_to(self.path))
            if suffix == ".vhd":
                lib = "work"
                exe(f'set_global_assignment -name {t:s} "{f:s}" -hdl_version VHDL_2008 -library {lib:s}')
            else:
                exe(f'set_global_assignment -name {t:s} "{f:s}"')

    def synthAll(self):
        assert self.top is not None
        self._defaultTclImports()
        exe = self.executor.exeCmd
        exe(f'execute_module -tool ipg')
        exe(f'execute_module -tool map')

        self._report.setSynthFileNames()

    def implemAll(self):
        self._defaultTclImports()
        exe = self.executor.exeCmd
        exe(f'execute_module -tool fit')
        exe(f'execute_module -tool sta')

        self._report.setImplFileNames()

    def writeBitstream(self):
        self._defaultTclImports()
        exe = self.executor.exeCmd
        exe('execute_module -tool asm')
        self._report.setBitstreamFileName()

    def close(self):
        exe = self.executor.exeCmd
        exe('project_close')

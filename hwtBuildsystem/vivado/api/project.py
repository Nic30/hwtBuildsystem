import os
from typing import Optional, Union

from hwtBuildsystem.common.project import SynthesisToolProject
from hwtBuildsystem.vivado.api import Language, FILE_TYPE
from hwtBuildsystem.vivado.report import VivadoReport
from hwtBuildsystem.vivado.api.tcl import VivadoTCL
import xml.etree.ElementTree as ET
from hwtBuildsystem.vivado.api.boardDesign import VivadoBoardDesign
from hwtBuildsystem.vivado.part import XilinxPart


class VivadoProject(SynthesisToolProject):
    SUFFIX_TO_FILE_TYPE = {
        ".v": FILE_TYPE.VERILOG,
        ".vhd": FILE_TYPE.VHDL_2008,
        ".vh": FILE_TYPE.VERILOG_HEADER,
        ".svh": FILE_TYPE.VERILOG_HEADER,
        ".sv": FILE_TYPE.SYSTEMVERILOG,
        ".edif": FILE_TYPE.EDIF,
        ".ngc": FILE_TYPE.NGC,
        ".tcl": FILE_TYPE.TCL,
    }

    def __init__(self, executor: "VivadoExecutor", path, name):
        """
        :param path: path is path of directory where project is stored
        :name name: name of project folder and project *.xpr/ppr file
        """
        self.executor = executor
        self.name = name
        j = os.path.join
        self.path = j(path, name)
        self.projFile = j(path, name, name + ".xpr")
        self.srcDir = j(path, name, name + ".srcs/sources_1")  # [TODO] needs to be derived from fs or project
        self.bdSrcDir = j(self.srcDir, 'bd')
        self.constrFileSet_name = 'constrs_1'
        self.part = None
        self.top = None
        self._report = VivadoReport(self.path, self.name, None)

    def create(self, in_memory=False):
        exe = self.executor.exeCmd
        exe(VivadoTCL.create_project(self.path, self.name, in_memory=in_memory))
        self.setTargetLangue(Language.vhdl)
        if self.executor.workerCnt is not None:
            exe(f"set_param general.maxThreads {self.executor.workerCnt:d}")

    def get(self):
        return "[current_project]"

    def updateAllCompileOrders(self):
        exe = self.executor.exeCmd
        for g in self.listFileGroups():
            exe(VivadoTCL.update_compile_order(g))

    def run(self, jobName: str, to_step:Optional[str]=None):
        exe = self.executor.exeCmd
        exe(VivadoTCL.reset_run(jobName))
        exe(VivadoTCL.launch_runs([jobName], workerCnt=self.executor.workerCnt, to_step=to_step))
        exe(VivadoTCL.wait_on_run(jobName))

    def synthAll(self):
        for s in self.listSynthesis():
            self.run(s)
        self._report.setSynthFileNames()

    # def synth(self, quiet=False):
    #    assert(self.top is not None)
    #    yield VivadoTCL.synth_design(self.top, self.part)

    def implemAll(self):
        for s in self.listIpmplementations():
            self.run(s)
        self._report.setImplFileNames()

    def writeBitstream(self):
        self.run("impl_1", to_step="write_bitstream")  # impl_1 -to_step write_bitstream -jobs 8
        self._report.setBitstreamFileName()

    def listRuns(self):
        tree = ET.parse(self.projFile)
        root = tree.getroot()
        for runs in root:
            if runs.tag != "Runs":
                continue
            for run in runs:
                assert run.tag == "Run"
                yield run

    def listSynthesis(self):
        for r in self.listRuns():
            if "Synth" in r.attrib["Type"]:
                yield r.attrib["Id"]

    def listIpmplementations(self):
        for r in self.listRuns():
            if "EntireDesign" in r.attrib["Type"]:
                yield r.attrib["Id"]

    def listFileGroups(self):
        tree = ET.parse(self.projFile)
        root = tree.getroot()
        for fss in root:
            if fss.tag != "FileSets":
                continue
            for fs in fss:
                assert fs.tag == "FileSet"
                yield fs.attrib["Name"]

    def setPart(self, part: Union[XilinxPart, str]):
        if isinstance(part, XilinxPart):
            partName = part.name()
        else:
            assert isinstance(part, str), part
            partName = part

        self.part = partName
        exe = self.executor.exeCmd
        exe(VivadoTCL.set_property(self.get(), "part", partName))

    def setIpRepoPaths(self, paths):
        exe = self.executor.exeCmd
        exe(VivadoTCL.set_property(self.get(), name='ip_repo_paths', valList=paths))
        exe(VivadoTCL.update_ip_catalog())

    def open(self):
        exe = self.executor.exeCmd
        exe(VivadoTCL.open_project(self.projFile))

    def close(self):
        exe = self.executor.exeCmd
        exe(VivadoTCL.close_project())

    def boardDesign(self, name) -> VivadoBoardDesign:
        return VivadoBoardDesign(self, name)

    def addFiles(self, files):
        exe = self.executor.exeCmd
        file_names = []
        file_types = []
        for f in files:
            if isinstance(f, tuple):
                f, t = f
            else:
                assert isinstance(f, str)
                suffix = os.path.splitext(f)[1].lower()
                if suffix == ".xdc":
                    exe(VivadoTCL.add_files([f, ],
                          fileSet=self.constrFileSet_name,
                          norecurse=True))
                    continue
                else:
                    t = self.SUFFIX_TO_FILE_TYPE[suffix]
            file_names.append(f)
            file_types.append(t)

        if not file_names:
            return

        exe(VivadoTCL.add_files(file_names))
        for f, t in zip(file_names, file_types):
            # set_property FILE_TYPE {VHDL 2008} [get_files x.vhd]
            exe(VivadoTCL.set_property(f'[get_files {f:s}]', "FILE_TYPE", f"{{{t:s}}}"))
        exe(VivadoTCL.update_compile_order("sources_1"))

    def setTop(self, topName):
        self.top = topName
        self._report.topName = topName
        exe = self.executor.exeCmd
        exe(VivadoTCL.set_property("[current_fileset]", 'top', topName))

    def addConstrainObjects(self, name, constrains):
        filename = os.path.join(self.srcDir, name + '.xdc')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write('\n'.join(map(lambda xdc: xdc.asTcl(), constrains)))

        self.addFiles([filename, ])

    def setTargetLangue(self, lang):
        assert(lang == Language.verilog or lang == Language.vhdl)
        exe = self.executor.exeCmd
        exe(VivadoTCL.set_property(self.get(), "target_language", lang))


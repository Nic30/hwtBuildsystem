import os
import shutil
from typing import Optional

from hwtBuildsystem.vivado.api import Language, FILE_TYPE
from hwtBuildsystem.vivado.api.boardDesign import BoardDesign
from hwtBuildsystem.vivado.report import VivadoReport
from hwtBuildsystem.vivado.tcl import VivadoTCL
import xml.etree.ElementTree as ET


class VivadoProject():

    def __init__(self, executor: "VivadoExecutor", path, name):
        """
        @param path: path is path of directory where project is stored
        @name name: name of project folder and project *.xpr/ppr file
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
        yield VivadoTCL.create_project(self.path, self.name, in_memory=in_memory)
        yield from self.setTargetLangue(Language.vhdl)
        if self.executor.workerCnt is not None:
            yield f"set_param general.maxThreads {self.executor.workerCnt:d}"

    def setFileType(self, fileName: str, fileType:FILE_TYPE):
        """
        set_property FILE_TYPE {VHDL 2008} [get_files x.vhd]
        """
        yield VivadoTCL.set_property(f'[get_files {fileName:s}]', "FILE_TYPE", f"{{{fileType:s}}}")

    def _exists(self):
        return os.path.exists(self.path)

    def _remove(self):
        shutil.rmtree(self.path)

    def get(self):
        return "[current_project]"

    def updateAllCompileOrders(self):
        for g in self.listFileGroups():
            yield VivadoTCL.update_compile_order(g)

    def run(self, jobName: str, to_step:Optional[str]=None):
        yield VivadoTCL.reset_run(jobName)
        yield VivadoTCL.launch_runs([jobName], workerCnt=self.executor.workerCnt, to_step=to_step)
        yield VivadoTCL.wait_on_run(jobName)

    def synthAll(self):
        for s in self.listSynthesis():
            yield from self.run(s)
        self._report.setSynthFileNames()

    # def synth(self, quiet=False):
    #    assert(self.top is not None)
    #    yield VivadoTCL.synth_design(self.top, self.part)

    def implemAll(self):
        for s in self.listIpmplementations():
            yield from self.run(s)
        self._report.setImplFileNames()

    def writeBitstream(self):
        yield from self.run("impl_1", to_step="write_bitstream")  # impl_1 -to_step write_bitstream -jobs 8
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

    def setPart(self, partName: str):
        self.part = partName
        yield VivadoTCL.set_property(self.get(), "part", partName)

    def setIpRepoPaths(self, paths):
        yield VivadoTCL.set_property(self.get(), name='ip_repo_paths', valList=paths)
        yield VivadoTCL.update_ip_catalog()

    def open(self):
        yield VivadoTCL.open_project(self.projFile)

    def close(self):
        yield VivadoTCL.close_project()

    def boardDesign(self, name) -> BoardDesign:
        return BoardDesign(self, name)

    def addDesignFiles(self, files):
        yield VivadoTCL.add_files(files)
        yield VivadoTCL.update_compile_order("sources_1")

    def setTop(self, topName):
        self.top = topName
        self._report.topName = topName
        yield VivadoTCL.set_property("[current_fileset]", 'top', topName)

    def addXdcFile(self, filename: str):
        yield VivadoTCL.add_files([filename],
                                  fileSet=self.constrFileSet_name,
                                  norecurse=True)

    def addXDCs(self, name, XDCs):
        filename = os.path.join(self.srcDir, name + '.xdc')
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write('\n'.join(map(lambda xdc: xdc.asTcl(), XDCs)))

        yield from self.addXdcFile(filename)

    def setTargetLangue(self, lang):
        assert(lang == Language.verilog or lang == Language.vhdl)
        yield VivadoTCL.set_property(self.get(), "target_language", lang)

    def report(self):
        return self._report


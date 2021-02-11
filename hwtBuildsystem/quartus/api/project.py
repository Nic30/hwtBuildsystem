from hwtBuildsystem.vivado.api import Language
import os


class QuartusProject():

    def __init__(self, path, name, workerCnt=None):
        """
        @param path: path is path of directory where project is stored
        @name name: name of project folder and project *.xpr/ppr file
        """
        self.name = name
        j = os.path.join
        self.path = j(path, name)
        self.projFile = j(path, name, name + ".xpr")
        self.srcDir = j(path, name, name + ".srcs/sources_1")  # [TODO] needs to be derived from fs or project
        self.bdSrcDir = j(self.srcDir, 'bd')
        self.constrFileSet_name = 'constrs_1'
        self.part = None
        self.top = None
        self.workerCnt = workerCnt

    def create(self, part):
        yield f'project_new {self.name:s} -overwrite'
        # Set top level info
        family, device, top # todo
        yield f'set_global_assignment -name FAMILY "{family:s}"'
        yield f'set_global_assignment -name DEVICE {device:s}'
        yield f'set_global_assignment -name TOP_LEVEL_ENTITY {self.top:s}'
        # set_global_assignment -name SDC_FILE ''' + constraints_filepath +

        yield from self.setTargetLangue(Language.vhdl)
        if self.workerCnt is not None:
            yield f"set_param general.maxThreads {self.workerCnt:d}"

import os
import shutil


class SynthesisToolProject():

    def __init__(self, executor: "ToolExecutor", path:str, name:str):
        """
        :param path: path is path of directory where project is stored
        :param name: name of project folder and project *.xpr/ppr/qpr/qsf file
        """
        self.part = None
        self.top = None
        self.name = name
        self.executor = executor
        self.path = os.path.join(path, name)

    def _exists(self):
        return os.path.exists(self.path)

    def _remove(self):
        shutil.rmtree(self.path)

    def report(self):
        return self._report


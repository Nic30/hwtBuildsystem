

class ToolExecutor():
    """
    An abstract class for a tool executors.
    Tool executor is an object which controlls some external tool in real time on command-output basis.
    """

    def _process(self, cmd):
        raise NotImplementedError("Should be implemented in concrete implementation of this class")

    def project(self, root, name:str):
        raise NotImplementedError()

    def process(self, cmds):
        """
        Process a list of commands and return the results
        """
        results = []
        for cmd in cmds:
            res = self._process(cmd)
            results.append(res)
        return results


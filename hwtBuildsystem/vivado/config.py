import os
from hwtBuildsystem.fileUtils import which


class VivadoConfig():
    HOME = None
    _DEFAULT_HOME_LINUX = '/opt/Xilinx/Vivado'

    @classmethod
    def getHome(cls):
        if cls.HOME is not None:
            return cls.HOME
        try:
            vivadoHomes = os.listdir(VivadoConfig._DEFAULT_HOME_LINUX)
        except Exception:
            raise Exception("Can not find Vivado indtalation automaticaly, set up VivadoConfig.HOME")

        if len(vivadoHomes) != 1:
            raise Exception('Can not resolve default Vivado available are %s' % (str(vivadoHomes)))

        return os.path.join(cls._DEFAULT_HOME_LINUX, vivadoHomes[0])

    @classmethod
    def getExec(cls):
        exe = "vivado"
        if which(exe) is None:
            return os.path.join(cls.getHome(), "bin", "vivado")
        return exe


if __name__ == "__main__":
    print(VivadoConfig.getExec())

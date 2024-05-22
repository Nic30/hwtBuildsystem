import os
from hwtBuildsystem.fileUtils import which


class QuartusConfig():
    HOME = None
    _DEFAULT_HOME_LINUX = '/opt/intelFPGA'

    @classmethod
    def getHome(cls):
        if cls.HOME is not None:
            return cls.HOME
        try:
            quartusHomes = os.listdir(cls._DEFAULT_HOME_LINUX)
        except Exception:
            raise Exception("Can not find Quartus installation automatically, set up QuartusConfig.HOME")

        if len(quartusHomes) != 1:
            raise Exception('Can not resolve default Quartus available are %s' % (str(quartusHomes)))

        res = os.path.join(cls._DEFAULT_HOME_LINUX, quartusHomes[0], "quartus")
        assert os.path.exists(res), res
        return res

    @classmethod
    def getExec(cls):
        exe = "quartus_sh"
        if which(exe) is None:
            return os.path.join(cls.getHome(), "bin", "quartus_sh")
        return exe


if __name__ == "__main__":
    print(QuartusConfig.getExec())

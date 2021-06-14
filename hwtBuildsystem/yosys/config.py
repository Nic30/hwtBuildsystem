from hwtBuildsystem.fileUtils import which


class YosysConfig():
    _DEFAULT_LINUX = '/usr/bin/yosys'

    @classmethod
    def getExec(cls):
        exe = "yosys"
        if which(exe) is None:
            raise Exception('Can find yosys installation')
        return exe


if __name__ == "__main__":
    print(YosysConfig.getExec())

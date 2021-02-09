from hwtBuildsystem.vivado.tcl import VivadoTCL


class Net():

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def create(self):
        src = self.src.get()
        dst = self.dst.get()
        if self.src.hasSubIntf:
            yield VivadoTCL.connect_bd_intf_net(src, dst)
        else:
            yield VivadoTCL.connect_bd_net(src, dst)

    @classmethod
    def createMultipleFromDict(cls, netDict):
        for src, dst in netDict.items():
            if isinstance(dst, list) or isinstance(dst, tuple):  # if has multiple dst create net for all of them
                for d in dst:
                    yield from cls(src, d).create()
            else:
                yield from cls(src, dst).create()

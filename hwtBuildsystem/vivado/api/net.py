from hwtBuildsystem.vivado.api.tcl import VivadoTCL


class VivadoBoardDesignNet():

    def __init__(self, bd: 'VivadoBoardDesign', src, dst):
        self.bd = bd
        self.src = src
        self.dst = dst

    def create(self):
        src = self.src.get()
        dst = self.dst.get()
        exe = self.bd.project.executor.exeCmd
        if self.src.hasSubIntf:
            exe(VivadoTCL.connect_bd_intf_net(src, dst))
        else:
            exe(VivadoTCL.connect_bd_net(src, dst))

    @classmethod
    def createMultipleFromDict(cls, bd: 'VivadoBoardDesign', netDict):
        for src, dst in netDict.items():
            if isinstance(dst, list) or isinstance(dst, tuple):  # if has multiple dst create net for all of them
                for d in dst:
                    cls(bd, src, d).create()
            else:
                cls(bd, src, dst).create()

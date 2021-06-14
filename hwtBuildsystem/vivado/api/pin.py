from hwtBuildsystem.vivado.api.tcl import VivadoTCL


class VivadoBoardDesignPin():

    def __init__(self, bd, name, hasSubIntf=False):
        self.bd = bd
        self.name = name
        self.hasSubIntf = hasSubIntf

    def get(self):
        if self.hasSubIntf:
            return VivadoTCL.get_bd_intf_pins([self.name])
        else:
            return VivadoTCL.get_bd_pins([self.name])

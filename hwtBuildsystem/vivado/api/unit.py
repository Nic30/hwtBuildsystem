from hwtBuildsystem.vivado.api.tcl import VivadoTCL
from hwtBuildsystem.vivado.api.pin import VivadoBoardDesignPin


class VivadoBoardDesignUnit():

    def __init__(self, bd: 'VivadoBoardDesign', ipCore, name):
        self.bd = bd
        self.ipCore = ipCore
        self.name = name
        self.pins = {}

    def create(self):
        exe = self.bd.project.executor.exeCmd
        exe(VivadoTCL.create_bd_cell(self.ipCore, self.name))

    def get(self):
        return VivadoTCL.get_bd_cells([self.name])

    def pin(self, name, hasSubIntf=False) -> VivadoBoardDesignPin:
        realPinName = "/%s/%s" % (self.name, name)
        p = self.pins.get(realPinName, None)
        if p:
            return p
        else:
            p = VivadoBoardDesignPin(self.bd, realPinName, hasSubIntf=hasSubIntf)
            self.pins[realPinName] = p
            return p

    def set(self, config):
        exe = self.bd.project.executor.exeCmd
        exe(VivadoTCL.set_property(VivadoTCL.get_bd_cells([self.name]), valDict=config))


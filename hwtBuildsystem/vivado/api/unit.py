from hwtBuildsystem.vivado.tcl import VivadoTCL
from hwtBuildsystem.vivado.api.pin import Pin


class VivadoUnit():

    def __init__(self, bd, ipCore, name):
        self.bd = bd
        self.ipCore = ipCore
        self.name = name
        self.pins = {}

    def create(self):
        yield VivadoTCL.create_bd_cell(self.ipCore, self.name)

    def get(self):
        return VivadoTCL.get_bd_cells([self.name])

    def pin(self, name, hasSubIntf=False):
        realPinName = "/%s/%s" % (self.name, name)
        p = self.pins.get(realPinName, None)
        if p:
            return p
        else:
            p = Pin(self.bd, realPinName, hasSubIntf=hasSubIntf)
            self.pins[realPinName] = p

            return p

    def set(self, config):
        yield VivadoTCL.set_property(VivadoTCL.get_bd_cells([self.name]), valDict=config)


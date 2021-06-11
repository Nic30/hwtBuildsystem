from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk, Rst, Rst_n
from hwtBuildsystem.vivado.tcl import VivadoTCL
from hwtBuildsystem.vivado.xdcGen import PortType
from ipCorePackager.constants import INTF_DIRECTION


class Port():

    def __init__(self, bd, name, direction=None, typ=None, hasSubIntf=False,
                 config=None, width=None, bitIndx=None):
        self.bd = bd
        self.name = name
        self.direction = direction
        self.typ = typ
        self.hasSubIntf = hasSubIntf
        if config is None:
            config = {}
        self.config = config
        self.extraXDC = []
        self.bitIndx = bitIndx
        self.width = width
        if width is not None:
            assert(not bitIndx)
            assert(width > 0)
            self.bits = [
                Port(bd, name, direction=direction, typ=typ, bitIndx=i)
                for i in range(width)
            ]
        else:
            self.bits = None

        if bitIndx is None and self.bd is not None:
            self.bd.insertPort(self)

    @classmethod
    def fromInterface(cls, interface: Signal):
        if isinstance(interface._dtype, Bits):
            width = interface._dtype.bit_length()
            if width == 1 and not interface._dtype.force_vector:
                width = None
        else:
            width = None
        if isinstance(interface, Clk):
            typ = PortType.clk
        elif isinstance(interface, (Rst, Rst_n)):
            typ = PortType.rst
        else:
            typ = None

        return cls(None, interface._getHdlName(),
                    direction=INTF_DIRECTION.asDirection(interface._direction),
                     typ=typ, hasSubIntf=bool(interface._interfaces),
                     width=width)

    def create(self):
        yield VivadoTCL.create_bd_port(self.name, self.direction,
                                       typ=self.typ, width=self.width)
        for k, v in self.config.items():
            yield VivadoTCL.set_property('[' + self.get() + ']', "CONFIG." + k, v)

    def forEachBit(self, fn):
        if self.bits:
            for bit in self.bits:
                fn(bit)
        else:
            fn(self)

    def get(self, forHdlWrapper=False):
        name = self.name
        if self.bitIndx is not None:
            name = "{%s[%d]}" % (name, self.bitIndx)

        names = [name]

        if forHdlWrapper:
            if self.hasSubIntf:
                raise NotImplemented()
            else:
                return VivadoTCL.get_ports(names)
        else:
            if self.hasSubIntf:
                return VivadoTCL.get_bd_intf_ports(names)
            else:
                return VivadoTCL.get_bd_ports(names)

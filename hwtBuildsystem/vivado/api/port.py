from hwt.hdl.types.bits import HBits
from hwt.hwIOs.std import HwIOSignal, HwIOClk, HwIORst, HwIORst_n
from hwtBuildsystem.vivado.api.tcl import VivadoTCL
from hwtBuildsystem.vivado.xdcGen import PortType
from ipCorePackager.constants import INTF_DIRECTION


class VivadoBoardDesignPort():

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
                VivadoBoardDesignPort(bd, name, direction=direction, typ=typ, bitIndx=i)
                for i in range(width)
            ]
        else:
            self.bits = None

        if bitIndx is None and self.bd is not None:
            self.bd.insertPort(self)

    @classmethod
    def fromInterface(cls, hwIO: HwIOSignal):
        if isinstance(hwIO._dtype, HBits):
            width = hwIO._dtype.bit_length()
            if width == 1 and not hwIO._dtype.force_vector:
                width = None
        else:
            width = None
        if isinstance(hwIO, HwIOClk):
            typ = PortType.clk
        elif isinstance(hwIO, (HwIORst, HwIORst_n)):
            typ = PortType.rst
        else:
            typ = None

        return cls(None, hwIO._getHdlName(),
                    direction=INTF_DIRECTION.asDirection(hwIO._direction),
                     typ=typ, hasSubIntf=bool(hwIO._hwIOs),
                     width=width)

    def create(self):
        exe = self.bd.project.executor.exeCmd

        exe(VivadoTCL.create_bd_port(self.name, self.direction,
                                     typ=self.typ, width=self.width))
        for k, v in self.config.items():
            exe(VivadoTCL.set_property('[' + self.get() + ']', "CONFIG." + k, v))

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

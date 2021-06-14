from mesonbuild.cmake.client import SignalBase

from hwt.constraints import iHdlConstrain, _get_absolute_path, _get_parent_unit
from hwt.serializer.xdc.serializer import XdcSerializer
from hwt.synthesizer.unit import Unit
from hwtBuildsystem.vivado.api.port import VivadoBoardDesignPort
from hwtBuildsystem.vivado.xdcGen import XdcPackagePin, XdcIoStandard


class set_IoPin(iHdlConstrain):
    """
    Placement constrain which specifies on which IO pin of the chip package will
    This signal be mapped.
    """

    def __init__(self, intf: SignalBase,
                 pin_map,
                 ommit_registration=False):
        assert not intf._interfaces
        assert len(pin_map) == intf._dtype.bit_length()
        self.pin_map = pin_map
        self.intf = _get_absolute_path(intf)
        if not ommit_registration:
            self.register_on_parent()

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        raise ValueError("The pin map is appliable only to a top thus any root reallocation should not be valid")

    def _get_parent(self) -> Unit:
        return _get_parent_unit(self.intf)

    @staticmethod
    def to_xdc(ser: XdcSerializer, self):
        s = self.intf[-1]
        p = VivadoBoardDesignPort.fromInterface(s)
        m = self.pin_map
        w = ser.out.write
        if p.bits:
            assert len(p.bits) == len(m), (s, m)
            for b, bm in zip(p.bits, m):
                w(XdcPackagePin(b, bm).asTcl())
                w("\n")
        else:
            assert len(m) == 1, (s, m)
            w(XdcPackagePin(p, m[0]).asTcl())
            w("\n")


class set_IoStandard(iHdlConstrain):

    def __init__(self, intf: SignalBase,
                 ioStd: XdcIoStandard,
                 ommit_registration=False):
        self.ioStd = ioStd
        self.intf = _get_absolute_path(intf)
        if not ommit_registration:
            self.register_on_parent()

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        return set_IoPin._copy_with_root_upadate(self, old_path_prefix, new_path_prefix)

    def _get_parent(self) -> Unit:
        return set_IoPin._get_parent(self)

    @staticmethod
    def to_xdc(ser: XdcSerializer, self):
        s = self.intf[-1]
        w = ser.out.write
        p = VivadoBoardDesignPort.fromInterface(s)
        ioStd = self.ioStd
        if p.bits:
            for b in p.bits:
                w(XdcIoStandard(b, ioStd).asTcl())
                w("\n")
        else:
            w(XdcIoStandard(p, ioStd).asTcl())
            w("\n")

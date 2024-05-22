
from typing import Optional, Union

from hwt.constraints import iHdlConstrain, _get_absolute_path, _get_parent_HwModule
from hwt.hwIOs.std import HwIOSignal, HwIOClk
from hwt.serializer.xdc.serializer import XdcSerializer
from hwt.hwModule import HwModule
from hwt.mainBases import RtlSignalBase
from hwtBuildsystem.vivado.api.port import VivadoBoardDesignPort
from hwtBuildsystem.vivado.xdcGen import XdcPackagePin, XdcIoStandard
from hwtSimApi.constants import Time
from hwtSimApi.utils import freq_to_period


class ConstrainIo(iHdlConstrain):
    """
    Placement constrain which specifies on which IO pin of the chip package will
    this signal be mapped to and which standard it will use and optionally also input clock frequency.

    :note: io standard specifies the voltange, logic type etc.
    """

    def __init__(self, hwIO: RtlSignalBase,
                 pin_map,
                 std: Union[XdcIoStandard, str, None],
                 ommit_registration=False):
        assert not hwIO._hwIOs
        assert len(pin_map) == hwIO._dtype.bit_length()
        self.pin_map = pin_map
        self.io_std = std
        self.hwIO = _get_absolute_path(hwIO)
        if not ommit_registration:
            self.register_on_parent()

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        raise ValueError("The pin map is appliable only to a top thus any root reallocation should not be valid")

    def _get_parent(self) -> HwModule:
        return _get_parent_HwModule(self.hwIO)

    @staticmethod
    def to_xdc(ser: XdcSerializer, self):
        hwIO = self.hwIO[-1]
        p = VivadoBoardDesignPort.fromInterface(hwIO)
        pin = self.pin_map
        std = self.ioStd
        w = ser.out.write
        if p.bits:
            # multibit vector like std_logic_vector wire[x:0]
            width = len(p.bits)
            if pin is None:
                pin = (None for _ in range(width))
            else:
                assert len(pin) == width, (pin, self.hwIO)

            if std is None:
                std = (None for _ in range(width))
            elif isinstance(std, str):
                std = (std for _ in range(width))
            else:
                assert len(std) == width, (std, self.hwIO)

            for b, bpin, bstd in zip(p.bits, pin):
                if bpin is not None:
                    w(XdcPackagePin(b, bpin).asTcl())
                    w("\n")

                if bstd is not None:
                    w(XdcIoStandard(b, bstd).asTcl())
                    w("\n")
        else:
            if isinstance(hwIO, HwIOClk):
                name = hwIO._phy_name
                period = freq_to_period(hwIO.FREQ) / Time.ns
                w(f'create_clock -name {name:s} -period {period:f} [get_ports {name}]\n')

            # 1b scalar like std_logic or wire/reg
            if pin is not None:
                assert len(pin) == 1, (hwIO, pin)
                w(XdcPackagePin(p, pin[0]).asTcl())
                w("\n")

            if std is not None:
                w(XdcIoStandard(p, std).asTcl())
                w("\n")

    @staticmethod
    def to_sdc(ser: 'SdcSeraializer', self: 'set_Io'):
        hwIO = self.hwIO[-1]
        pin = self.pin_map
        std = self.io_std
        w = ser.out.write
        name = hwIO._phy_name
        if isinstance(HwIOSignal):
            width = hwIO._dtype.bit_length()
            if width == 1 and not hwIO._dtype.force_vector:
                if isinstance(hwIO, HwIOClk):
                    period = freq_to_period(hwIO.FREQ) / Time.ns
                    w(f'create_clock -name "{name:s}" -period {period:f}ns [get_ports {{{name:s}}}]\n')

                if pin is not None:
                    w('set_location_assignment ')
                    w(pin)
                    w(' -to ')
                    w(name)
                    w('\n')

                if std is not None:
                    w('set_instance_assignment -name IO_STANDARD "')
                    w(std)
                    w('" -to ')
                    w(name)
                    w('\n')

            else:
                if pin is None:
                    pin = (None for _ in range(width))
                else:
                    assert len(pin) == width, (pin, hwIO)

                if std is None:
                    std = (None for _ in range(width))
                elif isinstance(std, str):
                    std = (std for _ in range(width))
                else:
                    assert len(std) == width, (std, hwIO)

                for i, bpin, bstd in enumerate(zip(pin, std)):
                    if bpin is not None:
                        w('set_location_assignment ')
                        w(bpin)
                        w(' -to ')
                        w(name)
                        w(f'[{i:d}]')
                        w('\n')

                    if bstd is not None:
                        w('set_instance_assignment -name IO_STANDARD "')
                        w(bstd)
                        w('" -to ')
                        w(name)
                        w(f'[{i:d}]')
                        w('\n')
        else:
            raise NotImplementedError()


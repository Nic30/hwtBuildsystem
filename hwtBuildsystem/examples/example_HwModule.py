from hwt.code import If
from hwt.hdl.types.bits import HBits
from hwt.hwIOs.std import HwIODataRdVld, HwIOBramPort_noClk
from hwt.hwIOs.utils import addClkRstn
from hwt.hwParam import HwParam
from hwt.hwModule import HwModule
from hwtBuildsystem.ioConstraints import ConstrainIo
from hwtBuildsystem.vivado.xdcGen import XdcIoStandard
from hwt.pyUtils.typingFuture import override
# from hwtBuildsystem.vivado.part import XilinxPart
# from hwtBuildsystem.quartus.part import IntelPart


class ExampleTop0(HwModule):
    """
    Lorem Ipsum componet to have something to compile
    """

    @override
    def hwConfig(self):
        self.DATA_WIDTH = HwParam(2)

    @override
    def hwDeclr(self):
        addClkRstn(self)
        with self._hwParamsShared():
            self.a = HwIODataRdVld()
            self.b = HwIODataRdVld()._m()

        r = self.ram_port = HwIOBramPort_noClk()
        r.ADDR_WIDTH = 10
        r.DATA_WIDTH = 8

    @override
    def hwImpl(self):
        a, b = self.a, self.b
        vld = self._reg("vld_delayed", def_val=0)
        vld(a.vld)
        b.vld(vld)
        b.data(a.data + 1)
        a.rd(b.rd & ~vld)

        ram_port = self.ram_port
        ram = self._sig("ram", HBits(8)[1024])
        If(self.clk._onRisingEdge(),
            If(ram_port.en,
               ram_port.dout(ram[ram_port.addr])
            ),
            If(ram_port.en & ram_port.we,
               ram[ram_port.addr](ram_port.din)
            ),
        )

        #def r(row, start, last):
        #    a = []
        #    for x in range(start, last + 1):
        #        a.append(row + ("%d" % x))
        #    return a
        #
        #def p(hwIO, pinMap, ioStd=XdcIoStandard.LVCMOS18):
        #    ConstrainIo(hwIO, pinMap, ioStd)
        #
        #if isinstance(self._target_platform, XilinxVivadoPlatform):
        #    assert self._target_platform.part == XilinxPart(
        #            XilinxPart.Family.kintex7,
        #            XilinxPart.Size._160t,
        #            XilinxPart.Package.ffg676,
        #            XilinxPart.Speedgrade._2)
        #    p(a.data, r("A", 8, 10) + r("A", 12, 15) + ["B9"])
        #    p(a.rd, ["B12", ])
        #    p(a.vld, ["B14", ])
        #
        #    p(b.data, ["B15", "C9"] + r("C", 11, 12) + ["C14"] + r("D", 8, 10))
        #    p(b.rd, ["D14", ])
        #    p(b.vld, ["E10", ])
        #    raise NotImplementedError("clk, rst_n and ram_port")
        #elif isinstance(self._target_platform, IntelPart):
        #    raise NotImplementedError()

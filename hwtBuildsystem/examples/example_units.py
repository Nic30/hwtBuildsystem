from hwt.code import If
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Handshaked, BramPort_withoutClk
from hwt.interfaces.utils import addClkRstn
from hwt.synthesizer.param import Param
from hwt.synthesizer.unit import Unit
from hwtBuildsystem.ioConstraints import ConstrainIo
from hwtBuildsystem.vivado.xdcGen import XdcIoStandard
# from hwtBuildsystem.vivado.part import XilinxPart
# from hwtBuildsystem.quartus.part import IntelPart


class ExampleTop0(Unit):
    """
    Lorem Ipsum componet to have something to compile
    """

    def _config(self):
        self.DATA_WIDTH = Param(2)

    def _declr(self):
        addClkRstn(self)
        with self._paramsShared():
            self.a = Handshaked()
            self.b = Handshaked()._m()

        r = self.ram_port = BramPort_withoutClk()
        r.ADDR_WIDTH = 10
        r.DATA_WIDTH = 8

    def _impl(self):
        a, b = self.a, self.b
        vld = self._reg("vld_delayed", def_val=0)
        vld(a.vld)
        b.vld(vld)
        b.data(a.data + 1)
        a.rd(b.rd & ~vld)

        ram_port = self.ram_port
        ram = self._sig("ram", Bits(8)[1024])
        If(self.clk._onRisingEdge(),
            If(ram_port.en,
               ram_port.dout(ram[ram_port.addr])
            ),
            If(ram_port.en & ram_port.we,
               ram[ram_port.addr](ram_port.din)
            ),
        )

        def r(row, start, last):
            a = []
            for x in range(start, last + 1):
                a.append(row + ("%d" % x))
            return a

        def p(intf, pinMap, ioStd=XdcIoStandard.LVCMOS18):
            ConstrainIo(intf, pinMap, ioStd)

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

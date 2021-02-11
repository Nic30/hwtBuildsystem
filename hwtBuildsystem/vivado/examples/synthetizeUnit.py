#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.ioConstraints import set_IoPin, set_IoStandard
from hwtBuildsystem.shortcuts import buildUnit
from hwtBuildsystem.vivado.logParser.synthesis import getLutFfLatchBramUramDsp
from hwtBuildsystem.vivado.xdcGen import IoStandard
from hwtLib.examples.simpleAxiStream import SimpleUnitAxiStream


class SimpleUnitAxiStreamTop(SimpleUnitAxiStream):

    def _impl(self):
        SimpleUnitAxiStream._impl(self)

        def r(row, start, last):
            a = []
            for x in range(start, last + 1):
                a.append(row + ("%d" % x))
            return a

        a, b = self.a, self.b

        def p(intf, pinMap, ioStd=IoStandard.LVCMOS18):
            set_IoPin(intf, pinMap)
            set_IoStandard(intf, ioStd)

        p(a.data, r("A", 8, 10) + r("A", 12, 15) + ["B9"])
        p(a.strb, ["B10"])
        p(a.last, ["B11", ])
        p(a.ready, ["B12", ])
        p(a.valid, ["B14", ])

        p(b.data, ["B15", "C9"] + r("C", 11, 12) + ["C14"] + r("D", 8, 10))
        p(b.strb, ["D11"])
        p(b.last, ["D13", ])
        p(b.ready, ["D14", ])
        p(b.valid, ["E10", ])


if __name__ == "__main__":
    u = SimpleUnitAxiStreamTop()
    r = buildUnit(u, "tmp", log=True,
                  synthesize=True,
                  implement=True,
                  writeBitstream=True,
                  # openGui=True,
                  )
    sr = r.parseUtilizationSynth()
    print(getLutFfLatchBramUramDsp(sr))
    print("Bitstream is in file %s" % (r.bitstreamFile))


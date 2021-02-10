#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, unittest
from unittest.case import TestCase
from hwtBuildsystem.vivado.logParser.synthesis import VivadoSynthesisLogParser, \
    getLutFfLatchBramUramDsp


def getFile(name):
    return os.path.join(os.path.dirname(__file__), name)


SimpleUnitAxiStreamTop_synth = getFile("SimpleUnitAxiStreamTop_utilization_synth.rpt")


class VivadoSynthLogParserTC(TestCase):

    def test_tableParsing(self):
        with open(SimpleUnitAxiStreamTop_synth) as f:
            p = VivadoSynthesisLogParser(f.read())
            p.parse()
        self.assertSequenceEqual(sorted(p.tables.keys()), [
            'Black Boxes',
            'Clocking',
            'DSP',
            'IO and GT Specific',
            'Instantiated Netlists',
            'Memory',
            'Primitives',
            'Slice Logic',
            'Specific Feature',
            'Summary of Registers by Type'])

    def test_tableData(self):
        with open(SimpleUnitAxiStreamTop_synth) as f:
            p = VivadoSynthesisLogParser(f.read())
            p.parse()
        d = getLutFfLatchBramUramDsp(p)
        self.assertDictEqual(d, {'lut': 0, 'ff': 0, 'latch': 0, 'bram': 0, 'uram': 0, 'dsp': 0})


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(VivadoSynthLogParserTC("test_VivadoErrorValidMsg"))
    suite.addTest(unittest.makeSuite(VivadoSynthLogParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

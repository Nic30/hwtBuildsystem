#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.case import TestCase

from hwtBuildsystem.quartus.logParser.synthesis import QuartusSynthesisLogParser
from tests.vivadoSynthLogParser_test import getFile

SimpleUnitAxiStreamTop_synth = getFile("SimpleUnitAxiStreamTop.map.rpt")


class QuartusSynthLogParserTC(TestCase):

    def test_tableParsing(self):
        with open(SimpleUnitAxiStreamTop_synth) as f:
            p = QuartusSynthesisLogParser(f.read())
            p.parse()
        self.assertSequenceEqual(sorted(p.tables.keys()), sorted([
            'Analysis & Synthesis Summary',
            'Analysis & Synthesis Settings',
            'Parallel Compilation',
            'Analysis & Synthesis Source Files Read',
            'Analysis & Synthesis Resource Usage Summary',
            'Analysis & Synthesis Resource Utilization by Entity',
            'General Register Statistics',
            'Parameter Settings for User Entity Instance: Top-level Entity: |SimpleUnitAxiStreamTop',
            'Post-Synthesis Netlist Statistics for Top Partition',
            'Elapsed Time Per Partition',
            'Analysis & Synthesis Messages',
            ]))

    def test_tableData(self):
        with open(SimpleUnitAxiStreamTop_synth) as f:
            p = QuartusSynthesisLogParser(f.read())
            p.parse()
        d = p.getBasicResourceReport()
        self.assertDictEqual(d, {'alm': 0, 'bram': 0, 'dsp': 0, 'ff': 0, 'latch': 0, 'lut': 0, 'uram': 0})


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(VivadoSynthLogParserTC("test_VivadoErrorValidMsg"))
    suite.addTest(unittest.makeSuite(QuartusSynthLogParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

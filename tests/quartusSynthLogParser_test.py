#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.case import TestCase

from hwtBuildsystem.quartus.logParser.synthesis import QuartusSynthesisLogParser
from tests.vivadoSynthLogParser_test import getFile, getFileFromTrace

ExampleTop0_synth_trace = getFile('ExampleTop0_synth_trace.quartus_arria10.json')
ExampleTop0_synth = getFileFromTrace(ExampleTop0_synth_trace, "tmp/quartus/ExampleTop0/ExampleTop0.map.rpt")


class QuartusSynthLogParserTC(TestCase):

    def test_tableParsing(self):
        p = QuartusSynthesisLogParser(ExampleTop0_synth)
        p.parse()
        self.assertSequenceEqual(sorted(p.tables.keys()), sorted([
                "Analysis & Synthesis Messages",
                "Analysis & Synthesis RAM Summary",
                "Analysis & Synthesis Resource Usage Summary",
                "Analysis & Synthesis Resource Utilization by Entity",
                "Analysis & Synthesis Settings",
                "Analysis & Synthesis Source Files Read",
                "Analysis & Synthesis Summary",
                "Elapsed Time Per Partition",
                "General Register Statistics",
                "Parallel Compilation",
                "Parameter Settings for Inferred Entity Instance: altsyncram:ram_rtl_0",
                "Parameter Settings for User Entity Instance: Top-level Entity: |ExampleTop0",
                "Post-Synthesis Netlist Statistics for Top Partition",
                "Registers Packed Into Inferred Megafunctions",
                "Source assignments for altsyncram:ram_rtl_0|altsyncram_9up1:auto_generated",
                "altsyncram Parameter Settings by Entity Instance",
            ]))

    def test_tableData(self):
        p = QuartusSynthesisLogParser(ExampleTop0_synth)
        p.parse()
        d = p.getBasicResourceReport()
        self.assertDictEqual(d, {'alm': 2, 'bram_bits': 8192, 'dsp': 0, 'ff': 1, 'latch': 0, 'lut': 4})


if __name__ == "__main__":
    testLoader = unittest.TestLoader()
    # suite = unittest.TestSuite([QuartusSynthLogParserTC("test_VivadoErrorValidMsg")])
    suite = testLoader.loadTestsFromTestCase(QuartusSynthLogParserTC)
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

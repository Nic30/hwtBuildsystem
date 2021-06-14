#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, unittest
from unittest.case import TestCase
from hwtBuildsystem.vivado.logParser.synthesis import VivadoSynthesisLogParser
from hwtBuildsystem.fakeTool.replayingExecutor import ReplayingExecutor
from hwtBuildsystem.examples.example_units import ExampleTop0
from hwtBuildsystem.examples.synthetizeUnit import buildUnit


def getFile(name):
    return os.path.join(os.path.dirname(__file__), name)


ExampleTop0_synth = getFile("ExampleTop0_utilization_synth.rpt")


class VivadoSynthLogParserTC(TestCase):

    def test_tableParsing(self):
        with open(ExampleTop0_synth) as f:
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
        with open(ExampleTop0_synth) as f:
            p = VivadoSynthesisLogParser(f.read())
            p.parse()
        d = p.getBasicResourceReport()
        self.assertDictEqual(d, {'lut': 0, 'ff': 0, 'latch': 0, 'bram': 0, 'uram': 0, 'dsp': 0})

    def test_parsingInProject(self):
        u = ExampleTop0()
        with ReplayingExecutor(getFile("ExampleTop0_synth_trace.json")) as v:
            r = buildUnit(v, u, "tmp",
                          synthesize=True,
                          implement=False,
                          writeBitstream=False,
                          # openGui=True,
                          )
            sr = r.parseUtilizationSynth().getBasicResourceReport()
            self.assertDictEqual(sr, {'lut': 0, 'ff': 0, 'latch': 0, 'bram': 0, 'uram': 0, 'dsp': 0})


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(VivadoSynthLogParserTC("test_VivadoErrorValidMsg"))
    suite.addTest(unittest.makeSuite(VivadoSynthLogParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

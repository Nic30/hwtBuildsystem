#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os, unittest
from unittest.case import TestCase

from hwtBuildsystem.examples.example_units import ExampleTop0
from hwtBuildsystem.examples.synthetizeUnit import buildUnit
from hwtBuildsystem.fakeTool.replayingExecutor import ReplayingExecutor
from hwtBuildsystem.vivado.logParser.synthesis import VivadoSynthesisLogParser
from hwtBuildsystem.vivado.part import XilinxPart


def getFile(name):
    return os.path.join(os.path.dirname(__file__), name)


def getFileFromTrace(trace_file_name, name):
    with open(trace_file_name) as tf:
        trace = json.load(tf)
        for _, files in reversed(trace['history']):
            for f_name, file_op in files:
                if f_name == name:
                    return file_op['text']
    raise ValueError(f"Trace file {trace_file_name:s} does not contain file {name:s}")


ExampleTop0_synth_trace = getFile("ExampleTop0_synth_trace.vivado_kintex7.json")
ExampleTop0_synth = getFileFromTrace(
    ExampleTop0_synth_trace,
    "tmp/vivado/ExampleTop0/ExampleTop0.runs/synth_1/ExampleTop0_utilization_synth.rpt")


class VivadoSynthLogParserTC(TestCase):

    def test_tableParsing(self):
        p = VivadoSynthesisLogParser(ExampleTop0_synth)
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
        p = VivadoSynthesisLogParser(ExampleTop0_synth)
        p.parse()
        d = p.getBasicResourceReport()
        self.assertDictEqual(d, {'lut': 3, 'ff': 1, 'latch': 0, 'bram': 0.5, 'uram': 0, 'dsp': 0})

    def test_parsingInProject(self):
        u = ExampleTop0()
        with ReplayingExecutor(ExampleTop0_synth_trace) as v:
            __pb = XilinxPart
            part = XilinxPart(
                    __pb.Family.kintex7,
                    __pb.Size._160t,
                    __pb.Package.ffg676,
                    __pb.Speedgrade._2)
            r = buildUnit(v, u, "tmp/vivado", part,
                          synthesize=True,
                          implement=False,
                          writeBitstream=False,
                          # openGui=True,
                          )
            sr = r.report().parseUtilizationSynth().getBasicResourceReport()
            self.assertDictEqual(sr, {'lut': 3, 'ff': 1, 'latch': 0, 'bram': 0.5, 'uram': 0, 'dsp': 0})


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(VivadoSynthLogParserTC("test_VivadoErrorValidMsg"))
    suite.addTest(unittest.makeSuite(VivadoSynthLogParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

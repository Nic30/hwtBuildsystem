#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import unittest
from unittest.case import TestCase

from hwtBuildsystem.yosys.logParser.synthesis import YosysSynthesisLogParser
from tests.vivadoSynthLogParser_test import getFile


def getCmdResFromTrace(trace_file_name, cmd_str):
    with open(trace_file_name) as tf:
        trace = json.load(tf)
        for cmd, _ in reversed(trace['history']):
            if cmd['cmd'] == cmd_str:
                return cmd['resultText']
    raise ValueError(f"Trace file {trace_file_name:s} does not contain command {cmd_str:s}")


ExampleTop0_synth_trace = getFile('ExampleTop0_synth_trace.yosys_ice40.json')
ExampleTop0_yosys_synth = getCmdResFromTrace(ExampleTop0_synth_trace, "synth_ice40 -top ExampleTop0 -json \"tmp/yosys/ExampleTop0/ExampleTop0.json\"")


class YosysSynthLogParserTC(TestCase):

    def test_tableParsing(self):
        p = YosysSynthesisLogParser(ExampleTop0_yosys_synth, 'ExampleTop0')
        p.parse()

        self.assertSequenceEqual(sorted(p.tables.keys()), sorted([
            'ExampleTop0',
            ]))

    def test_tableData(self):
        p = YosysSynthesisLogParser(ExampleTop0_yosys_synth, 'ExampleTop0')
        p.parse()
        d = p.getBasicResourceReport()
        self.assertDictEqual(d, {'bram': 2, 'dsp': 0, 'ff': 1, 'latch': 0, 'lut': 5, 'uram': 0})


if __name__ == "__main__":
    testLoader = unittest.TestLoader()
    # suite = unittest.TestSuite([YosysSynthLogParserTC("test_VivadoErrorValidMsg")])
    suite = testLoader.loadTestsFromTestCase(YosysSynthLogParserTC)
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

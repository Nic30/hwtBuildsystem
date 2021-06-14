#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.case import TestCase

from tests.vivadoSynthLogParser_test import getFile
from hwtBuildsystem.yosys.logParser.synthesis import YosysSynthesisLogParser

ExampleTop0_yosys_synth = getFile("ExampleTop0.yosys.synth.log")


class YosysSynthLogParserTC(TestCase):

    def test_tableParsing(self):
        with open(ExampleTop0_yosys_synth) as f:
            p = YosysSynthesisLogParser(f.read(), 'ExampleTop0')
            p.parse()

        self.assertSequenceEqual(sorted(p.tables.keys()), sorted([
            'ExampleTop0',
            ]))

    def test_tableData(self):
        with open(ExampleTop0_yosys_synth) as f:
            p = YosysSynthesisLogParser(f.read(), 'ExampleTop0')
            p.parse()
        d = p.getBasicResourceReport()
        self.assertDictEqual(d, {'lut': 8, 'bram': 0})


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(YosysSynthLogParserTC("test_VivadoErrorValidMsg"))
    suite.addTest(unittest.makeSuite(YosysSynthLogParserTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import tempfile
import unittest
from unittest.case import TestCase

from hwt.hwIOs.std import HwIOVectSignal
from hwt.hwParam import HwParam
from hwt.pyUtils.typingFuture import override
from hwtBuildsystem.cli_utils.hwModule_from_cli_args import hwModule_from_cli_args
from hwtLib.abstract.emptyHwModule import EmptyHwModule


class ParamEmptyHwModule(EmptyHwModule):
    DEFAULT_ARGS = [{"ADDR_WIDTH": 8, "DATA_WIDTH":32},
                    {"ADDR_WIDTH": 16, "DATA_WIDTH":32}]

    @override
    def hwConfig(self):
        self.ADDR_WIDTH = HwParam(8)
        self.DATA_WIDTH = HwParam(32)

    @override
    def hwDeclr(self):
        self.addr = HwIOVectSignal(self.ADDR_WIDTH)
        self.data = HwIOVectSignal(self.DATA_WIDTH)


class CLIUtilsTC(TestCase):

    def test_unit_from_cli_args_component_list(self):
        f = io.StringIO()
        hwModule_from_cli_args(ParamEmptyHwModule, ParamEmptyHwModule.DEFAULT_ARGS, ["-c"], stdout=f)
        output = f.getvalue()
        self.assertEqual(output.strip(), "ParamEmptyHwModule")

    def test_unit_from_cli_args_generic_list(self):
        f = io.StringIO()
        hwModule_from_cli_args(ParamEmptyHwModule, ParamEmptyHwModule.DEFAULT_ARGS, ["-g"], stdout=f)
        output = f.getvalue()
        self.assertEqual(output.strip(), "ADDR_WIDTH DATA_WIDTH")

    def test_unit_from_cli_args_file_list_default_unit_name(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:

            hwModule_from_cli_args(ParamEmptyHwModule,
                               ParamEmptyHwModule.DEFAULT_ARGS,
                               ["-f", "-l", "vhdl2008"],
                               out_folder=dirpath,
                               stdout=f)
            outFile = os.path.join(dirpath, "cli_utils_test/cli_utils_test.vhd")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)

    def test_unit_from_cli_args_file_list_vhdl(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:

            hwModule_from_cli_args(ParamEmptyHwModule,
                               ParamEmptyHwModule.DEFAULT_ARGS,
                               ["-f", "-l", "vhdl2008"],
                               out_folder=dirpath, unit_name="paramEmptyHwModule",
                                               stdout=f)
            outFile = os.path.join(dirpath, "paramEmptyHwModule/paramEmptyHwModule.vhd")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)

    def test_unit_from_cli_args_file_list_verilog(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:

            hwModule_from_cli_args(ParamEmptyHwModule,
                               ParamEmptyHwModule.DEFAULT_ARGS,
                               ["-f", "-l", "sv2012"],
                               out_folder=dirpath, unit_name="paramEmptyHwModule",
                               stdout=f)
            outFile = os.path.join(dirpath, "paramEmptyHwModule/paramEmptyHwModule.v")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)

    def test_unit_from_cli_args_basic_generation(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:
            hwModule_from_cli_args(ParamEmptyHwModule,
                               ParamEmptyHwModule.DEFAULT_ARGS,
                               ["-l", "vhdl2008",
                                "--ADDR_WIDTH", "8", "16", '32',
                                "--DATA_WIDTH", "32", "32", "32"],
                               out_folder=dirpath, unit_name="paramEmptyHwModule",
                               stdout=f)
            output = f.getvalue()
            self.assertEqual(output.strip(), "")
            outFile = os.path.join(dirpath, "paramEmptyHwModule/paramEmptyHwModule.vhd")
            refFileName = os.path.join(os.path.dirname(__file__), "paramEmptyHwModule.vhd")

            # with open(refFileName, 'w') as f, open(outFile) as of:
            #    f.write(of.read())

            with open(outFile) as of, open(refFileName) as refFile:
                self.assertListEqual(
                    list(of),
                    list(refFile))


if __name__ == "__main__":
    testLoader = unittest.TestLoader()
    suite = testLoader.loadTestsFromTestCase(CLIUtilsTC)
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

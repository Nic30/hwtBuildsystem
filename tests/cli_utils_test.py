#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
import tempfile
import unittest
from unittest.case import TestCase

from hwt.interfaces.std import VectSignal
from hwt.synthesizer.interfaceLevel.emptyUnit import EmptyUnit
from hwt.synthesizer.param import Param
from hwtBuildsystem.cli_utils.unit_from_cli_args import unit_from_cli_args



class ParamEmptyUnit(EmptyUnit):
    DEFAULT_ARGS = [{"ADDR_WIDTH": 8, "DATA_WIDTH":32},
                    {"ADDR_WIDTH": 16, "DATA_WIDTH":32}]

    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(32)

    def _declr(self):
        self.addr = VectSignal(self.ADDR_WIDTH)
        self.data = VectSignal(self.DATA_WIDTH)


class CLIUtilsTC(TestCase):

    def test_unit_from_cli_args_component_list(self):
        f = io.StringIO()
        unit_from_cli_args(ParamEmptyUnit, ParamEmptyUnit.DEFAULT_ARGS, ["-c"], stdout=f)
        output = f.getvalue()
        self.assertEqual(output.strip(), "ParamEmptyUnit")

    def test_unit_from_cli_args_generic_list(self):
        f = io.StringIO()
        unit_from_cli_args(ParamEmptyUnit, ParamEmptyUnit.DEFAULT_ARGS, ["-g"], stdout=f)
        output = f.getvalue()
        self.assertEqual(output.strip(), "ADDR_WIDTH DATA_WIDTH")

    def test_unit_from_cli_args_file_list_default_unit_name(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:

            unit_from_cli_args(ParamEmptyUnit,
                               ParamEmptyUnit.DEFAULT_ARGS,
                               ["-f", "-l", "vhdl2008"],
                               out_folder=dirpath,
                               stdout=f)
            outFile = os.path.join(dirpath, "cli_utils_test/cli_utils_test.vhd")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)

    def test_unit_from_cli_args_file_list_vhdl(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:

            unit_from_cli_args(ParamEmptyUnit,
                               ParamEmptyUnit.DEFAULT_ARGS,
                               ["-f", "-l", "vhdl2008"],
                               out_folder=dirpath, unit_name="paramEmptyUnit",
                                               stdout=f)
            outFile = os.path.join(dirpath, "paramEmptyUnit/paramEmptyUnit.vhd")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)

    def test_unit_from_cli_args_file_list_verilog(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:

            unit_from_cli_args(ParamEmptyUnit,
                               ParamEmptyUnit.DEFAULT_ARGS,
                               ["-f", "-l", "sv2012"],
                               out_folder=dirpath, unit_name="paramEmptyUnit",
                               stdout=f)
            outFile = os.path.join(dirpath, "paramEmptyUnit/paramEmptyUnit.v")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)

    def test_unit_from_cli_args_basic_generation(self):
        f = io.StringIO()
        with tempfile.TemporaryDirectory() as dirpath:
            unit_from_cli_args(ParamEmptyUnit,
                               ParamEmptyUnit.DEFAULT_ARGS,
                               ["-l", "vhdl2008",
                                "--ADDR_WIDTH", "8", "16", '32',
                                "--DATA_WIDTH", "32", "32", "32"],
                               out_folder=dirpath, unit_name="paramEmptyUnit",
                               stdout=f)
            output = f.getvalue()
            self.assertEqual(output.strip(), "")
            outFile = os.path.join(dirpath, "paramEmptyUnit/paramEmptyUnit.vhd")
            refFileName = os.path.join(os.path.dirname(__file__), "paramEmptyUnit.vhd")

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

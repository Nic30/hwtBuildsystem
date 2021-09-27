#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import os
from unittest.case import TestCase
from hwtBuildsystem.cli_utils.unit_from_cli_args import unit_from_cli_args
import contextlib
import tempfile
import unittest
from hwtLib.examples.axi.simpleAxiRegs import SimpleAxiRegs
from hwt.synthesizer.interfaceLevel.emptyUnit import EmptyUnit
from hwt.synthesizer.param import Param
from hwt.interfaces.std import VectSignal

class ParamEmptyUnit(EmptyUnit):
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(32)
        
    def _declr(self):
        self.addr = VectSignal(self.ADDR_WIDTH)
        self.data = VectSignal(self.DATA_WIDTH)

class CLIUtilsTC(TestCase):
    def test_unit_from_cli_args_component_list(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            unit_from_cli_args(ParamEmptyUnit, ["-c"])
            output = f.getvalue()
            self.assertEqual(output.strip(), "ParamEmptyUnit")

    def test_unit_from_cli_args_generic_list(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            unit_from_cli_args(ParamEmptyUnit, ["-g"])
            output = f.getvalue()
            self.assertEqual(output.strip(), "ADDR_WIDTH DATA_WIDTH")
            
    def test_unit_from_cli_args_file_list_default_unit_name(self):
        with contextlib.redirect_stdout(io.StringIO()) as f,\
            tempfile.TemporaryDirectory() as dirpath:
            
            unit_from_cli_args(ParamEmptyUnit, 
                               ["-f", "-l", "vhdl2008"], 
                               out_folder=dirpath)
            outFile = os.path.join(dirpath, "cli_utils_test/cli_utils_test.vhd")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)
            
    def test_unit_from_cli_args_file_list_vhdl(self):
        with contextlib.redirect_stdout(io.StringIO()) as f,\
            tempfile.TemporaryDirectory() as dirpath:
            
            unit_from_cli_args(ParamEmptyUnit, 
                               ["-f", "-l", "vhdl2008"], 
                               out_folder=dirpath, unit_name="paramEmptyUnit")
            outFile = os.path.join(dirpath, "paramEmptyUnit/paramEmptyUnit.vhd")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)
            
            
    def test_unit_from_cli_args_file_list_verilog(self):
        with contextlib.redirect_stdout(io.StringIO()) as f,\
            tempfile.TemporaryDirectory() as dirpath:
            
            unit_from_cli_args(ParamEmptyUnit, 
                               ["-f", "-l", "sv2012"], 
                               out_folder=dirpath, unit_name="paramEmptyUnit")
            outFile = os.path.join(dirpath, "paramEmptyUnit/paramEmptyUnit.v")
            output = f.getvalue()
            self.assertEqual(output.strip(), outFile)
            
            
    def test_unit_from_cli_args_basic_generation(self):
        f = io.StringIO()
        with contextlib.redirect_stdout(f),\
            tempfile.TemporaryDirectory() as dirpath:
            unit_from_cli_args(ParamEmptyUnit, ["-l", "vhdl2008",
                                               "--ADDR_WIDTH", "8", "16", '32',
                                               "--DATA_WIDTH", "32", "32", "32"], 
                                               out_folder=dirpath, unit_name="paramEmptyUnit")
            output = f.getvalue()
            self.assertEqual(output.strip(), "")
            outFile = os.path.join(dirpath, "paramEmptyUnit/paramEmptyUnit.vhd")
            self.assertListEqual(
                list(io.open(outFile)),
                list(io.open("paramEmptyUnit.vhd")))
            
            
if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CLIUtilsTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
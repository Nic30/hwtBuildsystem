#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.param import Param
from hwtBuildsystem.hwt.multiConfigUnit import MultiConfigUnitWrapper
from hwtLib.examples.hierarchy.hierarchySerialization_test import SimpleUnitWithParamWithIrrelevantParamAndAnotherParam
from hwtLib.examples.simpleWithParam import SimpleUnitWithParam
from tests.base_serialization_TC import BaseSerializationTC


class MultiConfigUnitWrapperTC(BaseSerializationTC):
    __FILE__ = __file__

    def test_MultiConfigUnitWrapper_same_io_type_different_int_param_vhdl(self):
        u0 = SimpleUnitWithParam()
        u0.DATA_WIDTH = 2
        u1 = SimpleUnitWithParam()
        u1.DATA_WIDTH = 3

        u = MultiConfigUnitWrapper([u0, u1])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_same_io_type_different_int_param.vhd")

    def test_MultiConfigUnitWrapper_same_io_type_different_int_param_verilog(self):
        u0 = SimpleUnitWithParam()
        u0.DATA_WIDTH = 2
        u1 = SimpleUnitWithParam()
        u1.DATA_WIDTH = 3

        u = MultiConfigUnitWrapper([u0, u1])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_same_io_type_different_int_param.v")

    def test_MultiConfigUnitWrapper_3x_same_io_type_different_int_param_vhdl(self):
        u0 = SimpleUnitWithParam()
        u0.DATA_WIDTH = 2
        u1 = SimpleUnitWithParam()
        u1.DATA_WIDTH = 3
        u2 = SimpleUnitWithParam()
        u2.DATA_WIDTH = 4

        u = MultiConfigUnitWrapper([u0, u1, u2])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_3x_same_io_type_different_int_param.vhd")

    def test_MultiConfigUnitWrapper_same_io_type_different_int_param_irrelevant_param_vhdl(self):

        class SimpleUnitWithParamWithIrrelevantParam(SimpleUnitWithParam):

            def _config(self):
                SimpleUnitWithParam._config(self)
                self.IRELEVANT_PARAM = Param(10)

        u0 = SimpleUnitWithParamWithIrrelevantParam()
        u0.DATA_WIDTH = 2
        u1 = SimpleUnitWithParamWithIrrelevantParam()
        u1.DATA_WIDTH = 3

        u = MultiConfigUnitWrapper([u0, u1])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_same_io_type_different_int_param_irrelevant_param.vhd")

    def test_MultiConfigUnitWrapper_same_io_type_different_int_param_irrelevant_param_and_second_param_vhdl(self):
        u0 = SimpleUnitWithParamWithIrrelevantParamAndAnotherParam()
        u0.ADDR_WIDTH = 11
        u0.DATA_WIDTH = 2

        u1 = SimpleUnitWithParamWithIrrelevantParamAndAnotherParam()
        u1.ADDR_WIDTH = 11
        u1.DATA_WIDTH = 3

        u2 = SimpleUnitWithParamWithIrrelevantParamAndAnotherParam()
        u2.ADDR_WIDTH = 13
        u2.DATA_WIDTH = 2

        u3 = SimpleUnitWithParamWithIrrelevantParamAndAnotherParam()
        u3.ADDR_WIDTH = 13
        u3.DATA_WIDTH = 3

        u = MultiConfigUnitWrapper([u0, u1, u2, u3])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_same_io_type_different_int_param_irrelevant_param_and_second_param.vhd")


if __name__ == "__main__":
    import unittest
    suite = unittest.TestSuite()
    # suite.addTest(MultiConfigUnitWrapperTC("test_MultiConfigUnitWrapper_same_io_type_different_int_param_verilog"))
    suite.addTest(unittest.makeSuite(MultiConfigUnitWrapperTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

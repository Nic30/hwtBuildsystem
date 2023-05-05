#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwt.synthesizer.interfaceLevel.emptyUnit import EmptyUnit
from hwt.synthesizer.param import Param
from hwtBuildsystem.hwt.multiConfigUnit import MultiConfigUnitWrapper
from hwtLib.amba.axi4Lite import Axi4Lite
from hwtLib.examples.hierarchy.hierarchySerialization_test import SimpleUnitWithParamWithIrrelevantParamAndAnotherParam
from hwtLib.examples.simpleWithParam import SimpleUnitWithParam
from tests.base_serialization_TC import BaseSerializationTC


class EmptyAxiLite(EmptyUnit):

    def _config(self) -> None:
        Axi4Lite._config(self)

    def _declr(self) -> None:
        with self._paramsShared():
            self.bus = Axi4Lite()


class MultiConfigUnitWrapperTC(BaseSerializationTC):
    __FILE__ = __file__

    def test_same_io_type_different_int_param_vhdl(self):
        u0 = SimpleUnitWithParam()
        u0.DATA_WIDTH = 2
        u1 = SimpleUnitWithParam()
        u1.DATA_WIDTH = 3

        u = MultiConfigUnitWrapper([u0, u1])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_same_io_type_different_int_param.vhd")

    def test_same_io_type_different_int_param_verilog(self):
        u0 = SimpleUnitWithParam()
        u0.DATA_WIDTH = 2
        u1 = SimpleUnitWithParam()
        u1.DATA_WIDTH = 3

        u = MultiConfigUnitWrapper([u0, u1])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_same_io_type_different_int_param.v")

    def test_3x_same_io_type_different_int_param_vhdl(self):
        u0 = SimpleUnitWithParam()
        u0.DATA_WIDTH = 2
        u1 = SimpleUnitWithParam()
        u1.DATA_WIDTH = 3
        u2 = SimpleUnitWithParam()
        u2.DATA_WIDTH = 4

        u = MultiConfigUnitWrapper([u0, u1, u2])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_3x_same_io_type_different_int_param.vhd")

    def test_same_io_type_different_int_param_irrelevant_param_vhdl(self):

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

    def test_same_io_type_different_int_param_irrelevant_param_and_second_param_vhdl(self):
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

    def test_Axi4Lite(self):
        u0 = EmptyAxiLite()
        u0.ADDR_WIDTH = 11
        u0.DATA_WIDTH = 16

        u1 = EmptyAxiLite()
        u1.ADDR_WIDTH = 12
        u1.DATA_WIDTH = 16

        u2 = EmptyAxiLite()
        u2.ADDR_WIDTH = 13
        u2.DATA_WIDTH = 16

        u = MultiConfigUnitWrapper([u0, u1, u2])
        self.assert_serializes_as_file(u, "MultiConfigUnitWrapper_Axi4Lite.vhd")


if __name__ == "__main__":
    import unittest
    testLoader = unittest.TestLoader()
    # suite = unittest.TestSuite([MultiConfigUnitWrapperTC("test_Axi4Lite")])
    suite = testLoader.loadTestsFromTestCase(MultiConfigUnitWrapperTC)
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

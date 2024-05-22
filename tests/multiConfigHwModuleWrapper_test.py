#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtLib.abstract.emptyHwModule import EmptyHwModule
from hwt.hwParam import HwParam
from hwtBuildsystem.hwt.multiConfigHwModule import MultiConfigHwModuleWrapper
from hwtLib.amba.axi4Lite import Axi4Lite
from hwtLib.examples.hierarchy.hierarchySerialization_test import SimpleHwModuleWithParamWithIrrelevantParamAndAnotherParam
from hwtLib.examples.simpleHwModuleWithHwParam import SimpleHwModuleWithHwParam
from tests.base_serialization_TC import BaseSerializationTC


class EmptyAxiLite(EmptyHwModule):

    def _config(self) -> None:
        Axi4Lite._config(self)

    def _declr(self) -> None:
        with self._hwParamsShared():
            self.bus = Axi4Lite()


class MultiConfigHwModuleWrapperTC(BaseSerializationTC):
    __FILE__ = __file__

    def test_same_io_type_different_int_param_vhdl(self):
        m0 = SimpleHwModuleWithHwParam()
        m0.DATA_WIDTH = 2
        m1 = SimpleHwModuleWithHwParam()
        m1.DATA_WIDTH = 3

        m = MultiConfigHwModuleWrapper([m0, m1])
        self.assert_serializes_as_file(m, "MultiConfigHwModuleWrapper_same_io_type_different_int_param.vhd")

    def test_same_io_type_different_int_param_verilog(self):
        m0 = SimpleHwModuleWithHwParam()
        m0.DATA_WIDTH = 2
        m1 = SimpleHwModuleWithHwParam()
        m1.DATA_WIDTH = 3

        m = MultiConfigHwModuleWrapper([m0, m1])
        self.assert_serializes_as_file(m, "MultiConfigHwModuleWrapper_same_io_type_different_int_param.v")

    def test_3x_same_io_type_different_int_param_vhdl(self):
        m0 = SimpleHwModuleWithHwParam()
        m0.DATA_WIDTH = 2
        m1 = SimpleHwModuleWithHwParam()
        m1.DATA_WIDTH = 3
        m2 = SimpleHwModuleWithHwParam()
        m2.DATA_WIDTH = 4

        m = MultiConfigHwModuleWrapper([m0, m1, m2])
        self.assert_serializes_as_file(m, "MultiConfigHwModuleWrapper_3x_same_io_type_different_int_param.vhd")

    def test_same_io_type_different_int_param_irrelevant_param_vhdl(self):

        class SimpleHwModuleWithParamWithIrrelevantParam(SimpleHwModuleWithHwParam):

            def _config(self):
                SimpleHwModuleWithHwParam._config(self)
                self.IRELEVANT_PARAM = HwParam(10)

        m0 = SimpleHwModuleWithParamWithIrrelevantParam()
        m0.DATA_WIDTH = 2
        m1 = SimpleHwModuleWithParamWithIrrelevantParam()
        m1.DATA_WIDTH = 3

        m = MultiConfigHwModuleWrapper([m0, m1])
        self.assert_serializes_as_file(m, "MultiConfigHwModuleWrapper_same_io_type_different_int_param_irrelevant_param.vhd")

    def test_same_io_type_different_int_param_irrelevant_param_and_second_param_vhdl(self):
        m0 = SimpleHwModuleWithParamWithIrrelevantParamAndAnotherParam()
        m0.ADDR_WIDTH = 11
        m0.DATA_WIDTH = 2

        m1 = SimpleHwModuleWithParamWithIrrelevantParamAndAnotherParam()
        m1.ADDR_WIDTH = 11
        m1.DATA_WIDTH = 3

        m2 = SimpleHwModuleWithParamWithIrrelevantParamAndAnotherParam()
        m2.ADDR_WIDTH = 13
        m2.DATA_WIDTH = 2

        u3 = SimpleHwModuleWithParamWithIrrelevantParamAndAnotherParam()
        u3.ADDR_WIDTH = 13
        u3.DATA_WIDTH = 3

        m = MultiConfigHwModuleWrapper([m0, m1, m2, u3])
        self.assert_serializes_as_file(m, "MultiConfigHwModuleWrapper_same_io_type_different_int_param_irrelevant_param_and_second_param.vhd")

    def test_Axi4Lite(self):
        m0 = EmptyAxiLite()
        m0.ADDR_WIDTH = 11
        m0.DATA_WIDTH = 16

        m1 = EmptyAxiLite()
        m1.ADDR_WIDTH = 12
        m1.DATA_WIDTH = 16

        m2 = EmptyAxiLite()
        m2.ADDR_WIDTH = 13
        m2.DATA_WIDTH = 16

        m = MultiConfigHwModuleWrapper([m0, m1, m2])
        self.assert_serializes_as_file(m, "MultiConfigHwModuleWrapper_Axi4Lite.vhd")


if __name__ == "__main__":
    import unittest
    testLoader = unittest.TestLoader()
    # suite = unittest.TestSuite([MultiConfigHwModuleWrapperTC("test_3x_same_io_type_different_int_param_vhdl")])
    suite = testLoader.loadTestsFromTestCase(MultiConfigHwModuleWrapperTC)
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

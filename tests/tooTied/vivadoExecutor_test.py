#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, unittest
from unittest.case import TestCase

from hwtBuildsystem.common.cmdResult import TclToolErr
from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.api.tcl import VivadoTCL


class VivadoExecutorTC(TestCase):

    def test_VivadoErrorPropagation(self):
        with self.assertRaises(TclToolErr):
            with VivadoExecutor() as v:
                v.exeCmd('dir')
                v.exeCmd('invalid_cmd_test')

    def test_VivadoErrorValidMsg(self):
        errRes = None
        with VivadoExecutor() as v:
            try:
                v.exeCmd('dir')
                v.exeCmd('invalid_cmd_test')
            except TclToolErr as e:
                errRes = e.args[0]

            self.assertTrue(errRes.resultText == '')
            self.assertTrue(errRes.errors[0] == 'invalid command name "invalid_cmd_test"')

    def test_warningParsing(self):
        with VivadoExecutor() as v:
            res = v.exeCmd('dir')
            self.assertEqual(len(res.errors), 0)
            self.assertEqual(len(res.criticalWarnings), 0)
            self.assertEqual(len(res.warnings), 1)
            self.assertEqual(len(res.infos), 0)

    def test_ls(self):
        with VivadoExecutor() as v:
            _pwd = v.exeCmd(VivadoTCL.pwd())
            _dir = v.exeCmd(VivadoTCL.ls())
            ls = [f for f in os.listdir(_pwd.resultText) if not f.startswith('.')]
            vivadoLs = _dir.resultText.split()
            ls.sort()
            vivadoLs.sort()
            self.assertListEqual(ls, vivadoLs)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(VivadoExecutorTC("test_VivadoErrorValidMsg"))
    suite.addTest(unittest.makeSuite(VivadoExecutorTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

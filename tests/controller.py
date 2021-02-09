import os, unittest
from unittest.case import TestCase

from hwtBuildsystem.vivado.cmdResult import VivadoErr
from hwtBuildsystem.vivado.controller import VivadoCntrl
from hwtBuildsystem.vivado.tcl import VivadoTCL


class ControllerTC(TestCase):

    def runCmds(self, cmds):
        with VivadoCntrl() as v:
            for _ in v.process(cmds):
                pass

    def test_VivadoErrorPropagation(self):
        self.assertRaises(VivadoErr, lambda: self.runCmds(['dir', 'invalid_cmd_test']))

    def test_VivadoErrorValidMsg(self):
        errRes = None
        try:
            self.runCmds(['dir', 'invalid_cmd_test'])
        except VivadoErr as e:
            errRes = e.cmdResult
        self.assertTrue(errRes.resultText == '')
        self.assertTrue(errRes.errors[0] == 'invalid command name "invalid_cmd_test"')

    def test_warningParsing(self):
        with VivadoCntrl() as v:
            res = list(v.process(['dir']))
            self.assertEqual(len(res), 1)
            res = res[0]
            self.assertEqual(len(res.errors), 0)
            self.assertEqual(len(res.criticalWarnings), 0)
            self.assertEqual(len(res.warnings), 1)
            self.assertEqual(len(res.infos), 0)

    def test_ls(self):
        with VivadoCntrl() as v:
            _pwd, _dir = v.process([VivadoTCL.pwd(), VivadoTCL.ls()])
            ls = os.listdir(_pwd.resultText)
            vivadoLs = _dir.resultText.split()
            ls.sort()
            vivadoLs.sort()
            self.assertListEqual(ls, vivadoLs)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(ControllerTC("test_VivadoErrorValidMsg"))
    suite.addTest(unittest.makeSuite(ControllerTC))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

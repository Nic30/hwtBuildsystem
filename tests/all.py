import unittest
from tests.vivadoSynthLogParser_test import VivadoSynthLogParserTC

ALL_TCs = [
    VivadoSynthLogParserTC,
]

if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(VivadoSynthLogParserTC("test_VivadoErrorValidMsg"))
    for tc in ALL_TCs:
        suite.addTest(unittest.makeSuite(tc))
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

import sys
import unittest

from tests.cli_utils_test import CLIUtilsTC
from tests.multiConfigUnitWrapper_test import MultiConfigUnitWrapperTC
from tests.quartusSynthLogParser_test import QuartusSynthLogParserTC
from tests.vivadoSynthLogParser_test import VivadoSynthLogParserTC
from tests.yosysSynthLogParser_test import YosysSynthLogParserTC

ALL_TCs = [
    VivadoSynthLogParserTC,
    QuartusSynthLogParserTC,
    YosysSynthLogParserTC,
    CLIUtilsTC,
    MultiConfigUnitWrapperTC,
]

if __name__ == "__main__":
    loader = unittest.TestLoader()
    loadedTcs = [loader.loadTestsFromTestCase(tc) for tc in ALL_TCs]
    suite = unittest.TestSuite(loadedTcs)

    runner = unittest.TextTestRunner(verbosity=3)
    res = runner.run(suite)

    if not res.wasSuccessful():
        sys.exit(1)

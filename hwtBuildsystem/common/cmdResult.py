import re
from typing import List


class TclToolErr(Exception):

    def __str__(self):
        return 'Cmd "%s" caused errors:\n%s' % (self.args[0].cmd, str(self.args[0].errors))


class TclCmdResult():
    """
    Parsed result of comand over cli
    """
    ANY_COLOR = r'((\033\[0m)?(\033\[0;(\d+)m)?\s*)?'
    OPT_MSG_NUMBER = r'(\s*\(\d+\))?'
    regex_invalidCmd = re.compile(r"(invalid command name \".*\")")
    regex_err = re.compile(f"{ANY_COLOR:s}ERROR{OPT_MSG_NUMBER:s}: (.*)")
    regex_critWarn = re.compile(f"{ANY_COLOR:s}CRITICAL WARNING{OPT_MSG_NUMBER:s}: (.*)")
    regex_warn = re.compile(f"{ANY_COLOR:s}WARNING{OPT_MSG_NUMBER:s}: (.*)")
    regex_info = re.compile(f"{ANY_COLOR:s}INFO{OPT_MSG_NUMBER:s}: (.*)")

    def __init__(self, cmd, resultText, errors, criticalWarnings, warnings, infos):
        self.cmd = cmd
        self.resultText = resultText
        self.errors = errors
        self.criticalWarnings = criticalWarnings
        self.warnings = warnings
        self.infos = infos

    @staticmethod
    def extractMsgs(msg, regex, err_str_group_i:int, listOfMsgs: List[str]):
        for m in regex.finditer(msg):
            listOfMsgs.append(m.group(err_str_group_i).strip())
        return regex.sub("", msg)

    @classmethod
    def fromStdoutStr(cls, cmd, text):
        resultText = text
        errors = []
        criticalWarnings = []
        warnings = []
        infos = []

        resultText = TclCmdResult.extractMsgs(resultText, TclCmdResult.regex_invalidCmd, 1, errors)
        resultText = TclCmdResult.extractMsgs(resultText, TclCmdResult.regex_err, 6, errors)
        resultText = TclCmdResult.extractMsgs(resultText, TclCmdResult.regex_critWarn, 6, criticalWarnings)
        resultText = TclCmdResult.extractMsgs(resultText, TclCmdResult.regex_warn, 6, warnings)
        resultText = TclCmdResult.extractMsgs(resultText, TclCmdResult.regex_info, 6, infos)

        return cls(cmd, resultText.strip(), errors, criticalWarnings, warnings, infos)

    def raiseOnErrors(self):
        if self.errors:
            raise TclToolErr(self)

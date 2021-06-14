import pexpect
from subprocess import check_output
from typing import Optional

from hwtBuildsystem.common.cmdResult import TclCmdResult
from hwtBuildsystem.common.executor import ToolExecutor
from hwtBuildsystem.yosys.api.project import YosysProject
from hwtBuildsystem.yosys.config import YosysConfig


class YosysExecutor(ToolExecutor):

    def __init__(self, execFile=None,
                 timeout=6 * 60 * 60,
                 logComunication=False,
                 workerCnt:Optional[int]=None):
        super(YosysExecutor, self).__init__(workerCnt)
        if execFile is None:
            execFile = YosysConfig.getExec()
        self.execFile = execFile
        self.proc = None
        self.timeout = timeout
        self.logComunication = logComunication
        self.encoding = 'ASCII'

    def getVersion(self):
        return check_output([self.execFile, '-V']).decode()

    def __enter__(self) -> 'YosysExecutor':
        cmd = []
        self.proc = pexpect.spawn(self.execFile, cmd)
        self.firstCmd = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        p = self.proc
        if p.isalive():
            p.sendline('exit')
            p.expect("exit", timeout=self.timeout)  # block while cmd ends

        if p.isalive():
            p.terminate()

    def exeCmd(self, cmd) -> TclCmdResult:
        p = self.proc
        if self.firstCmd:
            p.expect("yosys>", timeout=self.timeout)  # block while command line init
            self.firstCmd = False

        if self.logComunication:
            print(cmd)
        p.sendline(cmd)
        # @attention: there is timing issue in reading from tty next command returns corrupted line
        p.readline()  # read cmd from tty
        # p.expect(cmd, timeout=self.timeout)
        try:
            p.expect("yosys>", timeout=self.timeout)  # block while cmd ends
        except pexpect.EOF:
            pass
        t = p.before.decode(self.encoding)
        if self.logComunication:
            print(t, end="")
        res = TclCmdResult.fromStdoutStr(cmd, t)
        res.raiseOnErrors()
        return res

    def project(self, root, name) -> YosysProject:
        return YosysProject(self, root, name)


if __name__ == "__main__":
    with YosysExecutor(logComunication=True) as q:
        print(q.getVersion())
        h = q.exeCmd('help')
        print(h.resultText)
        err = q.exeCmd("xyz")

    print('finished')

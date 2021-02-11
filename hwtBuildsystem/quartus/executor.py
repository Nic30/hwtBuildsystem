import pexpect

from hwtBuildsystem.common.cmdResult import TclCmdResult
from hwtBuildsystem.common.executor import ToolExecutor
from hwtBuildsystem.quartus.config import QuartusConfig
from hwtBuildsystem.quartus.tcl import QuartusTCL


class QuartusExcutor(ToolExecutor):

    def __init__(self, execFile=QuartusConfig.getExec(),
                 timeout=6 * 60 * 60,
                 logComunication=False):
        self.execFile = execFile
        self.proc = None
        self.timeout = timeout
        self.logComunication = logComunication
        self.encoding = 'ASCII'

    def __enter__(self):
        cmd = ["-s"]
        self.proc = pexpect.spawn(self.execFile, cmd)
        self.firstCmd = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        p = self.proc
        if p.isalive():
            p.sendline(QuartusTCL.exit())
            p.expect("exit", timeout=self.timeout)  # block while cmd ends

        if p.isalive():
            p.terminate()

    def _process(self, cmd):
        p = self.proc
        if self.firstCmd:
            p.expect("tcl>", timeout=self.timeout)  # block while command line init
            self.firstCmd = False

        p.sendline(cmd)
        # @attention: there is timing issue in reading from tty next command returns corrupted line
        p.readline()  # read cmd from tty
        # p.expect(cmd, timeout=self.timeout)
        try:
            p.expect("tcl>", timeout=self.timeout)  # block while cmd ends
        except pexpect.EOF:
            pass
        t = p.before.decode(self.encoding)
        if self.logComunication:
            print(cmd)
            print(t)
        res = TclCmdResult.fromStdoutStr(cmd, t)
        res.raiseOnErrors()
        yield res


if __name__ == "__main__":
    with QuartusExcutor(logComunication=True) as q:
        _op, _pwd = q.process(['help', 'pwd', "xyz"])
        print(_op.resultText)
        print(_pwd.resultText)

    print('finished')

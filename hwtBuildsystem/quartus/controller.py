import os
import pexpect

from hwtBuildsystem.quartus.config import QuartusConfig
from hwtBuildsystem.quartus.tcl import QuartusTCL
from hwtBuildsystem.common.cmdResult import TclCmdResult


class QuartusCntrl():

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

    def _process(self, cmds):
        p = self.proc
        for cmd in cmds:
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

    def process(self, cmds, iterator=False):
        """
        @attention: if iterator == True you must iterate trough it to execute commands,
                    this is how python generator works
        @param iterator: return iterator over cmd results
        """
        results = self._process(cmds)
        if iterator:
            return results
        else:
            return list(results)

    def rmLogs(self):
        if os.path.exists(self.logFile):
            os.remove(self.logFile)
        if os.path.exists(self.jurnalFile):
            os.remove(self.jurnalFile)


if __name__ == "__main__":
    with QuartusCntrl(logComunication=True) as q:
        _op, _pwd = q.process(['help', 'pwd', "xyz"])
        print(_op.resultText)
        print(_pwd.resultText)

    print('finished')

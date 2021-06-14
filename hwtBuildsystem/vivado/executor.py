import os
import pexpect
from subprocess import check_output
from typing import Optional

from hwtBuildsystem.common.cmdResult import TclCmdResult
from hwtBuildsystem.common.executor import ToolExecutor
from hwtBuildsystem.vivado.api.project import VivadoProject
from hwtBuildsystem.vivado.config import VivadoConfig
from hwtBuildsystem.vivado.api.tcl import VivadoTCL


class VivadoExecutor(ToolExecutor):

    def __init__(self, execFile=None,
                 timeout=6 * 60 * 60,
                 jurnalFile:Optional[str]=None,
                 logFile:Optional[str]=None,
                 logComunication=False,
                 workerCnt:Optional[int]=None):
        super(VivadoExecutor, self).__init__(workerCnt)
        if execFile is None:
            execFile = VivadoConfig.getExec()
        self.execFile = execFile
        self.proc = None
        self.jurnalFile = jurnalFile
        self.logFile = logFile
        self.verbose = True
        self.timeout = timeout
        self.guiOpened = False
        self.logComunication = logComunication
        self.encoding = 'ASCII'

    def __enter__(self) -> 'VivadoExecutor':
        cmd = ["-mode", 'tcl' , "-notrace"]
        if self.verbose:
            cmd.append('-verbose')

        if self.jurnalFile is None:
            cmd.append("-nojournal")
        else:
            cmd.append(f"-journal {self.jurnalFile:s}")

        if self.logFile is None:
            cmd.append("-nolog")
        else:
            cmd.append(f"-log {self.logFile:s}")

        self.proc = pexpect.spawn(self.execFile, cmd)
        self.firstCmd = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        p = self.proc
        if p.isalive():
            p.sendline(VivadoTCL.exit())
            p.expect("exit", timeout=self.timeout)  # block while cmd ends

        if p.isalive():
            p.terminate()

    def openGui(self):
        """
       :attention: this method disconnects controller and opens gui
        """
        self.exeCmd(VivadoTCL.start_gui())
        if self.proc.isalive():
            self.proc.wait()

    def getVersion(self):
        return check_output([self.execFile, '-version']).decode()

    def exeCmd(self, cmd: str) -> TclCmdResult:
        p = self.proc
        if self.firstCmd:
            p.expect("Vivado%", timeout=self.timeout)  # block while command line init
            self.firstCmd = False
        if self.guiOpened:
            raise Exception("Controller have no acces to Vivado because gui is opened")

        p.sendline(cmd)
        # :attention: there is timing issue in reading from tty next command returns corrupted line
        p.readline()  # read cmd from tty
        # p.expect(cmd, timeout=self.timeout)
        if cmd == VivadoTCL.start_gui():
            self.guiOpened = True
        try:
            p.expect("Vivado%", timeout=self.timeout)  # block while cmd ends
        except pexpect.EOF:
            pass
        t = p.before.decode(self.encoding)
        if self.logComunication:
            print(cmd)
            print(t, end="")
        res = TclCmdResult.fromStdoutStr(cmd, t)
        res.raiseOnErrors()
        return res

    def project(self, root, name) -> VivadoProject:
        return VivadoProject(self, root, name)

    def rmLogs(self):
        if os.path.exists(self.logFile):
            os.remove(self.logFile)
        if os.path.exists(self.jurnalFile):
            os.remove(self.jurnalFile)


if __name__ == "__main__":
    """
    :note: An example of usage
    """
    with VivadoExecutor() as v:
        print(v.getVersion())
        _pwd = v.exeCmd('pwd')
        _dir = v.exeCmd('dir')
        ls = os.listdir(_pwd.resultText)
        vivadoLs = _dir.resultText.split()
        ls.sort()
        vivadoLs.sort()
        print(ls)
        print(vivadoLs)
        v.openGui()

    print('finished')

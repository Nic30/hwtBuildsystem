from collections import deque
import importlib
import json
import os
from pathlib import Path

from hwtBuildsystem.common.cmdResult import TclCmdResult
from hwtBuildsystem.common.executor import ToolExecutor
from hwtBuildsystem.common.project import SynthesisToolProject
from hwtBuildsystem.fakeTool.recordingExecutor import RecordingExecutor
from hwtBuildsystem.fakeTool.utils import RecordingExecutorJSON_decode_history, \
    RecordingExecutorJSON_decode


class ReplayingExecutor(ToolExecutor):
    """
    Replays the responses on commands as if it was a real tool.
    Also handles the update of previously traced files.
    """

    def __init__(self, traceFile: str, pwd=None):
        with open(traceFile) as fp:
            if pwd is None:
                pwd = os.getcwd()
            j = fp.read().replace(RecordingExecutor.VAR_NAME_PWD, pwd)
        rec = json.loads(j)
        self.history = deque(RecordingExecutorJSON_decode_history(rec['history']))
        self.initialFilesToWatch = RecordingExecutorJSON_decode(rec["filesToWatch"])
        execMod, execCls = rec['executorCls']
        self.executorCls = getattr(importlib.import_module(execMod), execCls)
        self.workerCnt = rec['workerCnt']

    def __enter__(self) -> 'ReplayingExecutor':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def exeCmd(self, cmd) -> TclCmdResult:
        res, fileOps = self.history.popleft()
        assert res.cmd == cmd, (res, cmd)
        for f, op in fileOps:
            if op.mode == 'd':
                os.remove(f)
            else:
                Path(f).parent.mkdir(parents=True, exist_ok=True)
                with open(f, op.mode) as _f:
                    _f.write(op.text)

        return res

    def project(self, root, name:str) -> SynthesisToolProject:
        return self.executorCls.project(self, root, name)

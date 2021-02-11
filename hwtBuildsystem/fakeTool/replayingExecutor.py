import importlib
import json
import os
from pathlib import Path

from hwtBuildsystem.common.executor import ToolExecutor
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
            j = fp.read().replace(RecordingExecutor.PWD_VAR_NAME, pwd)
        rec = json.loads(j)
        self.history = RecordingExecutorJSON_decode_history(rec['history'])
        self.initialFilesToWatch = RecordingExecutorJSON_decode(rec["filesToWatch"])
        self.cmdI = 0
        execMod, execCls = rec['executorCls']
        self.executorCls = getattr(importlib.import_module(execMod), execCls)
        self.workerCnt = rec['workerCnt']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _process(self, cmd: str):
        res, fileOps = self.history[self.cmdI][cmd]
        for f, op in fileOps:
            if op.mode == 'd':
                os.remove(f)
            else:
                Path(f).parent.mkdir(parents=True, exist_ok=True)
                with open(f, op.mode) as _f:
                    _f.write(op.text)

        self.cmdI += 1
        return res

    def project(self, root, name:str):
        return self.executorCls.project(self, root, name)

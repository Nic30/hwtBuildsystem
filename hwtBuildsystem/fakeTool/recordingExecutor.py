import json
import os
from typing import List

from hwtBuildsystem.common.cmdResult import TclCmdResult
from hwtBuildsystem.common.executor import ToolExecutor
from hwtBuildsystem.fakeTool.utils import FileOp, RecordingExecutorEncoder


class RecordingExecutor(ToolExecutor):
    PWD_VAR_NAME = "{% RecordingToolController.PWD_VAR_NAME %}"

    def __init__(self, executor: ToolExecutor,
                  filesToWatch:List[str],
                  traceFile: str,
                  pwd=None, removeAllTracedFilesFirst=True):
        self.workerCnt = executor.workerCnt
        if pwd is None:
            pwd = os.getcwd()
        self.pwd = pwd

        self.executor = executor
        ifs = self.initialFilesToWatch = {}
        fs = self.filesToWatch = {}
        for f in filesToWatch:
            if removeAllTracedFilesFirst:
                if os.path.exists(f):
                    os.remove(f)
                    stats = None
                else:
                    try:
                        stats = os.stat(f)
                    except FileNotFoundError:
                        stats = None

            if stats is not None:
                with open(f) as _f:
                    content = _f.read()
            else:
                content = ""
            fs[f] = (stats, content)

            if removeAllTracedFilesFirst and stats is not None:
                with open(f) as _f:
                    ifs[f] = FileOp('w', _f.read())
            else:
                ifs[f] = FileOp('d', None)

        self.traceFile = traceFile
        self.cmdI = 0
        self.history = {}

    def exeCmd(self, cmd) -> TclCmdResult:
        res = self.executor._process(cmd)
        fileChanges = []
        for f, (prev_st, prev_content) in self.filesToWatch.items():
            try:
                stats = os.stat(f)
            except FileNotFoundError:
                stats = None
            if stats != prev_st:
                if prev_st is None:
                    with open(f) as _f:
                        content = _f.read()
                    fileChanges.append([f, FileOp('w', content)])
                else:
                    raise NotImplementedError()

        self.history[self.cmdI] = {cmd: (res, fileChanges)}
        self.cmdI += 1
        return res

    def __enter__(self):
        self.executor.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.__exit__(exc_type, exc_val, exc_tb)
        with open(self.traceFile, "w") as fp:
            j = json.dumps({
                    "history": self.history,
                    "filesToWatch": self.initialFilesToWatch,
                    'executorCls': [self.executor.__class__.__module__, self.executor.__class__.__name__],
                    'workerCnt': self.workerCnt,
                },
                indent=2, separators=(',', ': '),
                cls=RecordingExecutorEncoder)
            j = j.replace(self.pwd, self.PWD_VAR_NAME)
            fp.write(j)

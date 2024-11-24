import json
import os
from typing import List

from hwtBuildsystem.common.cmdResult import TclCmdResult
from hwtBuildsystem.common.executor import ToolExecutor
from hwtBuildsystem.common.project import SynthesisToolProject
from hwtBuildsystem.fakeTool.utils import FileOp, RecordingExecutorEncoder
import re


class RecordingExecutor(ToolExecutor):
    VAR_NAME_PWD = "{% RecordingToolController.PWD %}"

    VAR_NAME_DATE = "{% RecordingToolController.NAME_DATE %}"
    RE_DATE = re.compile(r"[a-zA-Z]{3} [a-zA-Z]{3} \d+ \d+:\d+:\d+ \d{4}")

    VAR_NAME_VIVADO_MACHINE_RESOURCES = "{% RecordingToolController.VIVADO_MACHINE_RESOURCES %}"
    RE_VIVADO_MACHINE_RESOURCES = re.compile(r"Time \(s\): cpu = \d{2}:\d{2}:\d{2} ; elapsed = \d{2}:\d{2}:\d{2} . Memory \(MB\): peak = \d+.\d+ ; gain = \d+.\d+ ; free physical = \d+ ; free virtual = \d+")

    VAR_NAME_VIVADO_PROJECT_ID = "{% RecordingExecutor.VIVADO_PROJECT_ID %}"
    RE_VIVADO_PROJECT_ID = re.compile(r'(?<=<Option Name=\\"Id\\" Val=\\")[a-f0-9]{32}(?=\\"/>)')

    VAR_NAME_VIVADO_HELPER_PROC_PID = '{% RecordingExecutor.VIVADO_HELPER_PROC_PID %}'
    RE_VIVADO_HELPER_PROC_PID = re.compile(r'(?<=\[Synth 8-7075\] Helper process launched with PID )(\d+)')

    QUARTUS_INFO_TIMES = [
        (re.compile(r'(?<=Info: Peak virtual memory: )\d+(?= \S+)'),
         "{% RecordingExecutor.QUARTUS_PEAK_VIRT_MEM %}"),
        (re.compile(r'(?<=Info: Elapsed time: )\d{2}:\d{2}:\d{2}'),
         "{% RecordingExecutor.QUARTUS_ELAPSED_TIME %}"),
        (re.compile(r'(?<=Info: Total CPU time \(on all processors\): )\d{2}:\d{2}:\d{2}'),
         "{% RecordingExecutor.QUARTUS_TOTAL_CPU_TIME %}"),
    ]

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
        self.history = []

    def exeCmd(self, cmd) -> TclCmdResult:
        res = self.executor.exeCmd(cmd)
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

        self.history.append((res, fileChanges))
        return res

    def project(self, root, name:str) -> SynthesisToolProject:
        p = self.executor.project(root, name)
        p.executor = self
        return p

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
            j = j.replace(self.pwd, self.VAR_NAME_PWD)
            for (regex, sub) in [
                    (self.RE_DATE, self.VAR_NAME_DATE),
                    (self.RE_VIVADO_MACHINE_RESOURCES, self.VAR_NAME_VIVADO_MACHINE_RESOURCES),
                    (self.RE_VIVADO_PROJECT_ID, self.VAR_NAME_VIVADO_PROJECT_ID),
                    (self.RE_VIVADO_HELPER_PROC_PID, self.VAR_NAME_VIVADO_HELPER_PROC_PID),
                    *self.QUARTUS_INFO_TIMES,
                    ]:
                j = regex.sub(sub, j)

            fp.write(j)

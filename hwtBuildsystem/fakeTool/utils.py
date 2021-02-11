from hwtBuildsystem.common.cmdResult import TclCmdResult
from json.encoder import JSONEncoder
from copy import copy


class RecordingExecutorEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, (TclCmdResult, FileOp)):
            res = copy(o.__dict__)
            res["__class__"] = o.__class__.__name__
            return res
        else:
            return super(RecordingExecutorEncoder, self).default(o)


def RecordingExecutorJSON_decode_history(o):
    assert isinstance(o, dict), o
    return {
        int(k): RecordingExecutorJSON_decode(v)
        for k, v in o.items()
    }


def RecordingExecutorJSON_decode(o):
    if isinstance(o, dict):
        cls = o.get("__class__", "")
        if cls == TclCmdResult.__name__:
            return TclCmdResult(*(
                o.get(a, None)
                for a in ["cmd",
                          "resultText",
                          "errors",
                          "criticalWarnings",
                          "warnings",
                          "infos"]

            ))
        elif cls == FileOp.__name__:
            return FileOp(*(
                o.get(a, None)
                for a in ["mode",
                          "text", ]

            ))
        else:
            return {k: RecordingExecutorJSON_decode(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [RecordingExecutorJSON_decode(i) for i in o]
    else:
        return o


class FileOp():
    """
    An container of file operation for command history.
    """
    def __init__(self, mode, text):
        assert mode in ('w', 'a', 'd')
        self.mode = mode
        if mode == 'd':
            assert text is None
        self.text = text

    def apply(self, f):
        m = self.mode
        if m in ('a', 'w'):
            with open(f, m) as f:
                if self.text is not None:
                    f.write(self.text)


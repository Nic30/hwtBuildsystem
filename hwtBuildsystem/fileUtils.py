from contextlib import contextmanager
import os
from pathlib import Path


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


@contextmanager
def cd(newdir, create=False):
    prevdir = os.getcwd()
    newdir = os.path.expanduser(newdir)
    if create:
        Path(newdir).mkdir(parents=True, exist_ok=True)

    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)

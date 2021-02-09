from contextlib import contextmanager
import os
from pathlib import Path


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

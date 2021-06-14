#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.common.cmdResult import TclToolErr
from hwtBuildsystem.vivado.executor import VivadoExecutor


if __name__ == "__main__":
    with VivadoExecutor() as v:
        # process and show result
        cmdRes = v.exe_cmd('pwd')
        print(cmdRes.resultText)

        # show warnings
        if cmdRes.warnings:
            print(cmdRes.cmd + " caused warning(s):")
            print(cmdRes.warnings)

        # try invalid cmd
        try:
            v.exe_cmd('dafsadfa')
        except TclToolErr as e:
            print(e)

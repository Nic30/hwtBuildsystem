#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.controller import VivadoCntrl
from hwtBuildsystem.common.cmdResult import TclToolErr

if __name__ == "__main__":
    with VivadoCntrl() as v:
        # process and show result
        for cmdRes in  v.process(['dir', 'pwd'], iterator=True):
            print(cmdRes.resultText)

        # process and show only warnings
        for cmdRes in  v.process(['dir', 'pwd'], iterator=True):
            if cmdRes.warnings:
                print(cmdRes.cmd + " caused warning(s):")
                print(cmdRes.warnings)

        # try invalid cmd
        try:
            v.process(['dafsadfa'])
        except TclToolErr as e:
            print(e)

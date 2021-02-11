#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder


def importSampleBdProject(v: VivadoExecutor, part: str, tmpDir: str):
    p = v.project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()

    yield from p.create()
    yield from p.setPart(part)

    bd = p.boardDesign("test1")
    yield from bd.importFromTcl(tmpDir + 'test1.tcl', refrestTclIfExists=False)


if __name__ == "__main__":
    tmpDir = 'tmp/'
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()

    with VivadoExecutor(logComunication=True) as v:
        v.process(importSampleBdProject(v, part, tmpDir))
        v.openGui()

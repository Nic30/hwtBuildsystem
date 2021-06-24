#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.part import XilinxPart


def importSampleBdProject(v: VivadoExecutor, part: str, tmpDir: str):
    p = v.project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()

    p.create()
    p.setPart(part)

    bd = p.boardDesign("test1")
    bd.importFromTcl(tmpDir + 'test1.tcl', refrestTclIfExists=False)


if __name__ == "__main__":
    tmpDir = 'tmp/'
    pb = XilinxPart
    part = XilinxPart(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2)

    with VivadoExecutor(logComunication=True) as v:
        importSampleBdProject(v, part, tmpDir)
        v.openGui()

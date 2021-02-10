#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from hwtBuildsystem.vivado.controller import VivadoCntrl
from hwtBuildsystem.vivado.api.project import Project


def importSampleBdProject(tmpDir: str):
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()

    p = Project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()

    yield from p.create()
    yield from p.setPart(part)

    bd = p.boardDesign("test1")
    yield from bd.importFromTcl(tmpDir + 'test1.tcl', refrestTclIfExists=False)


if __name__ == "__main__":
    tmpDir = 'tmp/'
    with VivadoCntrl(logComunication=True) as v:
        v.process(importSampleBdProject(tmpDir))
        v.openGui()

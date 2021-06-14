#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from hwtBuildsystem.examples.vivado.createBdProject import examplePopulateBd


def createSampleBdProject(v: VivadoExecutor, tmpDir: str, part: str):
    p = v.project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()

    p.create()
    p.setPart(part)

    bd = p.boardDesign("test1")
    bd.create()
    examplePopulateBd(bd)
    bd.mkWrapper()
    bd.setAsTop()

    p.synthAll()


if __name__ == "__main__":
    tmpDir = "tmp"
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t,
                             pb.Package.ffg676, pb.Speedgrade._2).name()
    with VivadoExecutor(logComunication=True) as v:
        createSampleBdProject(v, tmpDir, part)
        v.openGui()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.examples.createBdProject import populateBd
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder


def createSampleBdProject(v: VivadoExecutor, tmpDir: str, part: str):
    p = v.project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()

    yield from p.create()
    yield from p.setPart(part)

    bd = p.boardDesign("test1")
    yield from bd.create()
    yield from populateBd(bd)
    yield from bd.mkWrapper()
    yield from bd.setAsTop()

    yield from p.synthAll()


if __name__ == "__main__":
    tmpDir = "tmp"
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t,
                             pb.Package.ffg676, pb.Speedgrade._2).name()
    with VivadoExecutor(logComunication=True) as v:
        v.process(createSampleBdProject(v, tmpDir, part))
        v.openGui()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.api.project import VivadoProject
from hwtBuildsystem.vivado.examples.createBdProject import populateBd
from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from hwtBuildsystem.vivado.xdcGen import PackagePin


def xdcForBd(bd, portMap):
    for port in bd.ports.values():
        pin = portMap[port.name.lower()]
        assert(isinstance(pin, str))
        yield PackagePin(port, pin)


def createSampleBdProject(v, tmpDir, part):
    p = v.project(tmpDir, "SampleBdProject" + part)
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
    portMap = {
        "portin": "C1",
        "portout": "C2"
    }

    yield from p.addXDCs('pinConstr', xdcForBd(bd, portMap))
    yield from p.implemAll()


if __name__ == "__main__":
    tmpDir = 'tmp/'
    pb = XilinxPartBuilder
    kintex = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()

    with VivadoExecutor(logComunication=True) as v:
        v.process(createSampleBdProject(v, tmpDir, kintex))
        v.openGui()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.controller import VivadoCntrl
from hwtBuildsystem.vivado.examples.createBdProject import populateBd
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from hwtBuildsystem.vivado.api.project import Project
from hwtBuildsystem.vivado.xdcGen import PackagePin


def xdcForBd(bd, portMap):
    for port in bd.ports.values():
        pin = portMap[port.name.lower()]
        assert(isinstance(pin, str))
        yield PackagePin(port, pin)


def createSampleBdProject(tmpDir, part):
    p = Project(tmpDir, "SampleBdProject" + part)
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


def processCommandsAndOpenGui(tmpDir, part):
    with VivadoCntrl(logComunication=True) as v:
        v.process(createSampleBdProject(tmpDir, part))
        v.openGui()


if __name__ == "__main__":
    tmpDir = 'tmp/'
    pb = XilinxPartBuilder
    kintex = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()
    zynq = XilinxPartBuilder(pb.Family.zynq7000, pb.Size._020, pb.Package.clg484, pb.Speedgrade._2).name()

    # processCommandsAndOpenGui(tmpDir, kintex)
    processCommandsAndOpenGui(tmpDir, zynq)


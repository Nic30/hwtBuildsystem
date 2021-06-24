#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict

from hwtBuildsystem.examples.vivado.createBdProject import examplePopulateBd
from hwtBuildsystem.vivado.api.boardDesign import VivadoBoardDesign
from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.part import XilinxPart
from hwtBuildsystem.vivado.xdcGen import XdcPackagePin


def xdcForBd(bd: VivadoBoardDesign, portMap: Dict[str, str]):
    for port in bd.ports.values():
        pin = portMap[port.name.lower()]
        assert(isinstance(pin, str))
        yield XdcPackagePin(port, pin)


def createSampleBdProject(v: VivadoExecutor, tmpDir: str, part: str):
    p = v.project(tmpDir, "SampleBdProject" + part)
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
    portMap = {
        "portin": "C1",
        "portout": "C2"
    }

    p.addConstrainObjects('pinConstr', xdcForBd(bd, portMap))
    p.implemAll()


if __name__ == "__main__":
    tmpDir = 'tmp/'
    pb = XilinxPart
    kintex = XilinxPart(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2)

    with VivadoExecutor(logComunication=True) as v:
        createSampleBdProject(v, tmpDir, kintex)
        v.openGui()


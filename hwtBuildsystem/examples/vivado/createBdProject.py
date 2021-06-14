#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hwtBuildsystem.vivado.api.boardDesign import VivadoBoardDesign
from hwtBuildsystem.vivado.api.net import VivadoBoardDesignNet
from hwtBuildsystem.vivado.api.port import VivadoBoardDesignPort
from hwtBuildsystem.vivado.executor import VivadoExecutor
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from ipCorePackager.constants import DIRECTION


def examplePopulateBd(bd: VivadoBoardDesign):
    p_in = VivadoBoardDesignPort(bd, "portIn", direction=DIRECTION.IN)
    p_in.create()

    p_out = VivadoBoardDesignPort(bd, "portOut", direction=DIRECTION.OUT)
    p_out.create()

    VivadoBoardDesignNet.createMultipleFromDict(bd, {p_out: p_in})


def createSampleBdProject(v: VivadoExecutor, tmpDir):
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()

    p = v.project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()

    p.create()
    p.setPart(part)

    bd = p.boardDesign("test1")
    bd.create()
    examplePopulateBd(bd)
    bd.mkWrapper()
    bd.exportToTCL(tmpDir + 'test1.tcl', force=True)


def showCommands(tmpDir: str):
    for cmd in createSampleBdProject(tmpDir):
        print(cmd)


if __name__ == "__main__":
    tmpDir = 'tmp/'

    print("#showCommands")
    showCommands(tmpDir)

    print("#processCommandsWithOpenedLogger")
    with VivadoExecutor(logComunication=True) as v:
        createSampleBdProject(v, tmpDir)

    print("processCommandsAndOpenGui")
    with VivadoExecutor(logComunication=True) as v:
        createSampleBdProject(v, tmpDir)
        v.openGui()

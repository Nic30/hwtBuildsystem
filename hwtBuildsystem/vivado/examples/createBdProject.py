from hwtBuildsystem.vivado.controller import VivadoCntrl
from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from ipCorePackager.constants import DIRECTION
from hwtBuildsystem.vivado.api.boardDesign import BoardDesign
from hwtBuildsystem.vivado.api.port import Port
from hwtBuildsystem.vivado.api.net import Net
from hwtBuildsystem.vivado.api.project import Project


def populateBd(bd: BoardDesign):
    p_in = Port(bd, "portIn", direction=DIRECTION.IN)
    yield from p_in.create()

    p_out = Port(bd, "portOut", direction=DIRECTION.OUT)
    yield from p_out.create()

    yield from Net.createMultipleFromDict({p_out: p_in})


def createSampleBdProject(tmpDir):
    pb = XilinxPartBuilder
    part = XilinxPartBuilder(pb.Family.kintex7, pb.Size._160t, pb.Package.ffg676, pb.Speedgrade._2).name()

    p = Project(tmpDir, "SampleBdProject")
    if p._exists():
        p._remove()

    yield from p.create()
    yield from p.setPart(part)

    bd = p.boardDesign("test1")
    yield from bd.create()
    yield from populateBd(bd)
    yield from bd.mkWrapper()
    yield from bd.exportToTCL(tmpDir + 'test1.tcl', force=True)


def showCommands(tmpDir: str):
    for cmd in createSampleBdProject(tmpDir):
        print(cmd)


def processCommandsWithOpenedLogger(tmpDir: str):
    with VivadoCntrl(logComunication=True) as v:
        v.process(createSampleBdProject(tmpDir))


def processCommandsAndOpenGui(tmpDir: str):
    with VivadoCntrl(logComunication=True) as v:
        v.process(createSampleBdProject(tmpDir))
        v.openGui()


if __name__ == "__main__":
    tmpDir = 'tmp/'

    print("#showCommands")
    showCommands(tmpDir)

    print("#processCommandsWithOpenedLogger")
    processCommandsWithOpenedLogger(tmpDir)

    print("processCommandsAndOpenGui")
    processCommandsAndOpenGui(tmpDir)

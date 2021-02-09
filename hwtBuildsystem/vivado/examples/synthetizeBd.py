from hwtBuildsystem.vivado.partBuilder import XilinxPartBuilder
from hwtBuildsystem.vivado.api import Project, Port, Net
from hwtBuildsystem.vivado.controller import VivadoCntrl
from hwtBuildsystem.vivado.samples.createBdProject import populateBd

tmpDir = 'tmp/'

def xdcForBd(bd, portMap):
    for _, p in bd.ports.items():
        yield from p.generateXDC(portMap)

def createSampleBdProject():
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
    yield from bd.setAsTop()
    
    yield from p.synth()
    
def processCommandsAndOpenGui():
    with VivadoCntrl(logComunication=True) as v:
        v.process(createSampleBdProject())
        v.openGui()

if __name__ == "__main__":
    processCommandsAndOpenGui()

import os
from hwtBuildsystem.vivado.tcl import VivadoTCL
from hwtBuildsystem.vivado.api import ConfigErr
from hwtBuildsystem.vivado.api.unit import VivadoUnit


class BoardDesign():

    def __init__(self, project, name=None):
        j = os.path.join
        self.project = project
        self.name = name
        self.bdDir = j(self.project.bdSrcDir, self.name)
        self.bdFile = j(self.bdDir, name + ".bd")
        self.bdWrapperFile = j(self.bdDir , 'hdl', self.name + "_wrapper.vhd")
        self.ports = {}

    def create(self):
        yield  VivadoTCL.create_bd_design(self.name)

    def delete(self, fromDisk=True):
        yield VivadoTCL.remove_files([self.bdFile])
        yield VivadoTCL.remove_files([self.bdWrapperFile])

        if fromDisk:
            yield VivadoTCL.file.delete([self.bdDir])
            yield VivadoTCL.file.delete([self.bdWrapperFile])

    def exist(self):
        return os.path.exists(self.bdFile)

    def open(self):
        yield VivadoTCL.open_bd_design(self.bdFile)

    def insertPort(self, port):
        name_l = port.name.lower()
        if name_l in self.ports:
            raise ConfigErr("%s port redefinition" % name_l)
        else:
            self.ports[name_l] = port

    def importFromTcl(self, fileName, refrestTclIfExists=True):
        """
        @param refrestIfExists: refresh tcl file from bd before opening design
        """
        p = os.path
        assert(self.name == p.splitext(p.basename(fileName))[0])  # assert name of bd in tcl is correct

        # update tcl from bd
        if p.exists(self.bdFile) and refrestTclIfExists:
            yield from self.open()
            yield from self.exportToTCL(fileName, force=True)

        # tcl file does not contains revisions of ips
        yield VivadoTCL.update_ip_catalog()

        # remove old bd
        yield from self.delete()

        # import new from tcl
        yield VivadoTCL.source(fileName)

        # generate wrapper and set is as top
        yield from self.mkWrapper()

    def exportToTCL(self, fileName, force=False):
        yield VivadoTCL.write_bd_tcl(fileName, force=force)

    def mkWrapper(self):
        yield VivadoTCL.make_wrapper(self.bdFile)
        yield VivadoTCL.add_files([self.bdWrapperFile])
        yield from self.project.updateAllCompileOrders()

    def setAsTop(self):
        yield from self.project.setTop(self.name + "_wrapper")

    def unit(self, name, ipCore=None):
        return VivadoUnit(name, ipCore=ipCore)

    def regenerateLayout(self):
        yield VivadoTCL.regenerate_bd_layout()


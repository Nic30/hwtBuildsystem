import os

from hwtBuildsystem.vivado.api import ConfigErr
from hwtBuildsystem.vivado.api.tcl import VivadoTCL
from hwtBuildsystem.vivado.api.unit import VivadoBoardDesignUnit


class VivadoBoardDesign():

    def __init__(self, project: 'VivadoProject', name=None):
        j = os.path.join
        self.project = project
        self.name = name
        self.bdDir = j(self.project.bdSrcDir, self.name)
        self.bdFile = j(self.bdDir, name + ".bd")
        self.bdWrapperFile = j(self.bdDir , 'hdl', self.name + "_wrapper.vhd")
        self.ports = {}

    def create(self):
        exe = self.project.executor.exeCmd
        exe(VivadoTCL.create_bd_design(self.name))

    def delete(self, fromDisk=True):
        exe = self.project.executor.exeCmd
        exe(VivadoTCL.remove_files([self.bdFile]))
        exe(VivadoTCL.remove_files([self.bdWrapperFile]))

        if fromDisk:
            exe(VivadoTCL.file.delete([self.bdDir]))
            exe(VivadoTCL.file.delete([self.bdWrapperFile]))

    def exist(self):
        return os.path.exists(self.bdFile)

    def open(self):
        exe = self.project.executor.exeCmd
        exe(VivadoTCL.open_bd_design(self.bdFile))

    def insertPort(self, port):
        name_l = port.name.lower()
        if name_l in self.ports:
            raise ConfigErr("%s port redefinition" % name_l)
        else:
            self.ports[name_l] = port

    def importFromTcl(self, fileName, refrestTclIfExists=True):
        """
        :param refrestIfExists: refresh tcl file from bd before opening design
        """
        p = os.path
        assert(self.name == p.splitext(p.basename(fileName))[0])  # assert name of bd in tcl is correct

        # update tcl from bd
        if p.exists(self.bdFile) and refrestTclIfExists:
            self.open()
            self.exportToTCL(fileName, force=True)

        exe = self.project.executor.exeCmd
        # tcl file does not contains revisions of ips
        exe(VivadoTCL.update_ip_catalog())

        # remove old bd
        self.delete()

        # import new from tcl
        exe(VivadoTCL.source(fileName))

        # generate wrapper and set is as top
        self.mkWrapper()

    def exportToTCL(self, fileName, force=False):
        exe = self.project.executor.exeCmd
        exe(VivadoTCL.write_bd_tcl(fileName, force=force))

    def mkWrapper(self):
        exe = self.project.executor.exeCmd
        exe(VivadoTCL.make_wrapper(self.bdFile))
        exe(VivadoTCL.add_files([self.bdWrapperFile]))
        self.project.updateAllCompileOrders()

    def setAsTop(self):
        return self.project.setTop(self.name + "_wrapper")

    def unit(self, name, ipCore=None) -> VivadoBoardDesignUnit:
        return VivadoBoardDesignUnit(name, ipCore=ipCore)

    def regenerateLayout(self):
        exe = self.project.executor.exeCmd
        exe(VivadoTCL.regenerate_bd_layout())


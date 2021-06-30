from typing import List, Optional

from ipCorePackager.constants import DIRECTION
from hwtBuildsystem.common.tcl import CommonTcl


# http://www.xilinx.com/support/documentation/sw_manuals/xilinx2013_1/ug975-vivado-quick-reference.pdf
class VivadoFSOpsTCL():

    @staticmethod
    def ls():
        return 'ls'

    @staticmethod
    def cd(path: str):
        return f'cd {path:s}'

    @staticmethod
    def pwd():
        return "pwd"

    class file():

        # file system manipulator
        @staticmethod
        def delete(files, force=True):
            if force:
                params = '-force'
            else:
                params = ""

            return "file delete %s %s" % (params, ' '.join(files))


class VivadoBDOpsTCL():
    # [TODO]
    # copy_bd_objs /  [get_bd_cells {c_accum_0}]
    # delete_bd_objs [get_bd_nets c_accum_0_Q] [get_bd_cells c_accum_0]

    @staticmethod
    def open_bd_design(fileName):
        return 'open_bd_design {%s}' % fileName

    @staticmethod
    def get_bd_ports(names):
        return 'get_bd_ports %s' % (' '.join(names))

    @staticmethod
    def create_bd_port(name: str,
                       direction: DIRECTION,
                       typ: Optional[str]=None,
                       width:Optional[int]=None):
        params = []

        if direction == DIRECTION.IN:
            d = "I"
        elif direction == DIRECTION.OUT:
            d = "O"
        else:
            raise Exception()

        params.append(f"-dir {d:s}")
        if width is not None:
            params.append('-from %s -to %d' % ((width - 1), 0))

        if typ != None:
            params.append(f"-type {typ:s}")

        return "create_bd_port %s %s" % (' '.join(params), name)

    @staticmethod
    def get_bd_intf_pins(names: List[str]):
        return 'get_bd_intf_pins %s' % (' '.join(names))

    @staticmethod
    def get_bd_intf_ports(names: List[str]):
        raise NotImplemented()

    @staticmethod
    def get_bd_pins(names):
        return 'get_bd_pins %s' % (' '.join(names))

    @staticmethod
    def create_bd_design(name: str):
        return f'create_bd_design "{name:s}"'

    @staticmethod
    def create_bd_cell(ipId: str, name: str):
        return f"create_bd_cell -type ip -vlnv {ipId:s} {name:s}"

    @staticmethod
    def make_wrapper(bdFile: str):
        # top has to be at end
        return f"make_wrapper -files [get_files {bdFile:s}] -top "

    @staticmethod
    def get_bd_cells(names: List[str]):
        return "[get_bd_cells %s]" % ' '.join(names)

    @staticmethod
    def connect_bd_net(src: str, dst: str):
        # connect_bd_net [get_bd_pins /eth0/txp] [get_bd_ports txp]
        return f"connect_bd_net [{src:s}] [{dst:s}]"

    @staticmethod
    def connect_bd_intf_net(src: str, dst: str):
        # connect_bd_intf_net [get_bd_intf_pins eth3a/m_axis_rx] [get_bd_intf_pins eth3a/s_axis_tx]
        return f"connect_bd_intf_net [{src:s}] [{dst:s}]"

    @staticmethod
    def regenerate_bd_layout():
        return "regenerate_bd_layout"

    @staticmethod
    def save_bd_design():
        return "save_bd_design"

    @staticmethod
    def write_bd_tcl(tclFileName, force=False):
        """save bd as independent tcl
           bd has to be saved and opened"""
        params = []
        if force:
            params.append('-force')
        return "write_bd_tcl %s %s" % (' '.join(params), tclFileName)


class VivadoProjectOpsTCL():

    @staticmethod
    def add_files(files, fileSet=None, norecurse=True):
        params = []
        if norecurse:
            params.append('-norecurse')
        if fileSet is not None:
            params.append(f"-fileset {fileSet:s}")
        return 'add_files %s %s' % (' '.join(params), ' '.join(files))

    @staticmethod
    def update_compile_order(fileSet):
        return "update_compile_order -fileset %s" % (fileSet)

    @staticmethod
    def generate_target(bdFile):
        return 'generate_target all [get_files  %s]' % (bdFile)

    class ip_repo_paths():

        @staticmethod
        def add(repoPath):
            """Multiple add will not cause duplicates"""
            return VivadoTCL.set_property("[current_project]", name="ip_repo_paths", value=repoPath)

    @staticmethod
    def remove_files(files):
        '''remove from project'''
        return "remove_files %s" % (' '.join(files))

    @staticmethod
    def update_ip_catalog(rebuild=True, scan_changes=True):
        params = []
        if rebuild:
            params.append('-rebuild')
        if scan_changes:
            params.append('-scan_changes')
        return "update_ip_catalog %s" % (' '.join(params))

    @staticmethod
    def open_project(filename: str):
        return f'open_project {filename:s}'

    @staticmethod
    def close_project():
        return 'close_project'

    @staticmethod
    def reset_run(name: str):
        return f"reset_run {name:s}"

    @staticmethod
    def launch_runs(names: List[str], workerCnt=None, to_step=None, quiet=False):
        assert names
        params = []
        if to_step is not None:
            params.append(f"-to_step {to_step:s}")
        if workerCnt is not None:
            params.append(f"-jobs {workerCnt:d}")
        if quiet:
            params.append("-quiet")

        if params:
            return "launch_runs %s %s" % (' '.join(names), ' '.join(params))
        else:
            return "launch_runs %s" % (' '.join(names))

    @staticmethod
    def run(jobName, workerCnt=None):
        return VivadoTCL.reset_run(jobName) + '\n' + \
               VivadoTCL.launch_runs(jobName, workerCnt=workerCnt)

    @staticmethod
    def wait_on_run(run, timeout=None):
        params = []
        if timeout is not None:
            params.append(f"-timeout {timeout:d}")

        return "wait_on_run %s %s" % (" ".join(params), run)

    @staticmethod
    def create_project(_dir, name, in_memory=False):
        """
        :param in_memory:     Create an in-memory project
        :param name:          Project name
        :param _dir:          Directory where the project file is saved
        """
        params = [name, _dir]
        if in_memory:
            params.append('-in_memory')

        return "create_project %s" % ' '.join(params)


class VivadoHdlOps():

    @staticmethod
    def get_ports(portNames):
        return "get_ports %s" % (" ".join(portNames))


class VivadoTCL(CommonTcl, VivadoFSOpsTCL, VivadoBDOpsTCL, VivadoProjectOpsTCL, VivadoHdlOps):
    """
    python wraps for Vivado TCL commands
    """

    @staticmethod
    def set_property(obj, name=None, value=None, valDict=None, valList=None):
        if valDict != None:
            valueStr = ' '.join(map(lambda kv: "%s {%s}" % (kv[0], str(kv[1])), valDict.items()))
            params = f"-dict [list {valueStr:s}]"
        elif value != None:
            params = "%s %s" % (name, str(value))
        elif valList != None:
            params = "%s {%s}" % (name, " ".join(valList))
        else:
            raise Exception()

        return f"set_property {params:s} {obj:s}"

    @staticmethod
    def source(scriptPath, noTrace=True):
        cmd = ["source", scriptPath]
        if noTrace:
            cmd.append('-notrace')
        return " ".join(cmd)

    @staticmethod
    def synth_design(top: str, part: str, quiet=False):
        if quiet:
            params = " -quiet"
        else:
            params = ""
        return f"synth_design -top {top:s} -part {part:s}{params:s}"

    class group():

        @staticmethod
        def start():
            return 'startgroup'

        @staticmethod
        def end():
            return 'endgroup'

    @staticmethod
    def start_gui():
        return "start_gui"

    class sim():

        # http://www.xilinx.com/support/answers/53351.html
        # https://gist.github.com/imrickysu/ad8318229a603f8c7e79
        # set_property top test_tb [get_filesets sim_1]
        # set_property top_lib xil_defaultlib [get_filesets sim_1]
        @staticmethod
        def launch():
            return "launch_simulation"

        @staticmethod
        def close():
            return "close_sim"

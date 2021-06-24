import os
from typing import Tuple, Union

from hwtBuildsystem.common.project import SynthesisToolProject
from hwtBuildsystem.yosys.report import YosysReport
from hwtBuildsystem.vivado.part import XilinxPart
from hwtBuildsystem.yosys.part import LatticePart
from hwtBuildsystem.quartus.part import IntelPart


class YosysProject(SynthesisToolProject):
    """
    API for controlling of the yosys project
    :note: The yosys does not have explicit project file, but in this context
        it means the api for control of the files, parts and executing of design runs
    """

    SUFFIX_TO_FILE_TYPE = {
        ".v": "-sv2012",
        ".vhd": "-vhdl2008",
        ".vh": "-sv2012",
        ".svh": "-sv2012",
        ".sv": "-sv2012",
    }

    def __init__(self, executor: "YosysProject", path:str, name:str):
        super(YosysProject, self).__init__(executor, path, name)
        self.name = name
        self._report = YosysReport(self.path, self.name, None)

    def setPart(self, part: Union[LatticePart, IntelPart, XilinxPart, Tuple[str, str, str]]):
        """
        :param part: vendor specific tuple
            IntelPart("Intel", "Cyclone", "EP1C12F256C6"),
            LaticePart('Lattice', 'iCE40', 'up5k', 'sg48')
        """
        self.part = part

    def setTop(self, topName):
        self.top = topName
        self._report.topName = topName

    def create(self):
        os.makedirs(self.path, exist_ok=True)
        # :note: the project is only virtual as writen in doc of this class

    def addFiles(self, files):
        # https://www.intel.com/content/www/us/en/programmable/documentation/eca1490998903550.html#mnl1088
        exe = self.executor.exeCmd
        for f in files:
            if isinstance(f, tuple):
                f, t = f
            else:
                suffix = os.path.splitext(f)[1].lower()
                t = self.SUFFIX_TO_FILE_TYPE[suffix]
            exe(f'read {t:s} "{f:s}"')

    def synthAll(self):
        assert self.top is not None
        exe = self.executor.exeCmd
        # http://www.clifford.at/yosys/documentation.html
        part = self.part
        cmd = None
        if part is None:
            cmd = 'synth'
        else:
            if isinstance(part, tuple):
                vendor = part[0].lower()
                default_cmds = {
                    'achronix': 'synth_achronix',  # Acrhonix Speedster22i FPGAs.
                    'gowin': 'synth_gowin',  #  Gowin FPGAs
                    'anlogic': 'synth_anlogic',  #  Anlogic FPGAs
                    'silego': 'synth_greenpak4',  # Silego GreenPAK4 FPGAs
                    'microchip': 'synth_sf2',  # microchip SmartFusion2 and IGLOO2 FPGAs
                }
                cmd = default_cmds.get(vendor, None)
            else:
                cmd = None

            if cmd is None:
                if isinstance(part, LatticePart):
                    if part.family == 'ECP5':
                        cmd = 'synth_ecp5'  # ECP5 FPGAs
                    elif part.family == 'iCE40':
                        cmd = 'synth_ice40'  # iCE40 FPGAs
                    else:
                        raise AssertionError("Unknown part family for Lattice chips (supported: ecp5, ice40)", part)
                elif isinstance(part, IntelPart):
                    if part.family == 'easic':
                        cmd = 'synth_easic'  # intel eASIC platform
                    else:
                        cmd = 'synth_intel'  # Intel (Altera) FPGAs.
                elif isinstance(part, XilinxPart):
                    if part.family == 'coolrunner2':
                        cmd = 'synth_coolrunner2'  # synthesis for Xilinx Coolrunner-II CPLDs
                    else:
                        cmd = 'synth_xilinx'  # synthesis for Xilinx FPGAs
                else:
                    raise AssertionError("Unknown part vendor", part)

        assert self.top, "Top entity must be specified first"
        out_json = os.path.join(self.path, self.top + '.json')
        r = exe(cmd + f' -top {self.top:s} -json "{out_json:s}"')
        self._report.setSynthLog(r.resultText)

    def implemAll(self):
        raise NotImplementedError("Need to implement for specifyc place&route backend")

    def writeBitstream(self):
        raise NotImplementedError("Need to implement for specifyc bitstream packer backend")

    def close(self):
        """
        The project was just virtual in the first place, no closing required.
        """
        pass

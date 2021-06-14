from hwtBuildsystem.vivado.api.tcl import VivadoTCL


class PortType():
    clk = "clk"
    rst = "rst"


class SimpleXDCProp():
    """
    xdc property setter container
    """

    def __init__(self, port, mode):
        self.port = port
        self.mode = mode

    def asTcl(self):
        return VivadoTCL.set_property('[' + self.port.get(forHdlWrapper=True) + ']', self._propName, self.mode)


class XdcVccAuxIo(SimpleXDCProp):
    _propName = "VCCAUX_IO"
    NORMAL = "NORMAL"
    DONTCARE = "DONTCARE"


class XdcSlew(SimpleXDCProp):
    _propName = "SLEW"
    FAST = "FAST"


class XdcLoc(SimpleXDCProp):
    _propName = "LOC"


class XdcPackagePin(SimpleXDCProp):
    _propName = 'PACKAGE_PIN'


class XdcIoStandard(SimpleXDCProp):
    """
    Io standard of pin thats mean setting of voltage, open-drain etc...
    """
    _propName = "IOSTANDARD"
    LVCMOS12 = "LVCMOS12"
    LVCMOS15 = "LVCMOS15"
    LVCMOS18 = "LVCMOS18"
    LVCMOS25 = 'LVCMOS25'
    HSTL_I_DCI = "HSTL_I_DCI"
    DIFF_HSTL_I = "DIFF_HSTL_I"
    HSTL_I = "HSTL_I"

# file:///opt/intelFPGA/18.0/quartus/common/help/webhelp/index.htm#reference/glossary/def_iostandard.htm


class XdcTextWrapper():
    """Wrapper around tcl in text"""

    def __init__(self, text):
        self.text = text

    def asTcl(self):
        return self.text


class XdcComment(XdcTextWrapper):
    """tcl xdc comment"""

    def __init__(self, text):
        super(XdcComment, self).__init__("#" + text)


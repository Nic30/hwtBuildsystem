class VivadoReport():
    """
    This class is output from hardware synthesis made by vivado
    All attributes are filenames
    """

    def __init__(self):
        # impl
        self.dcrOpted = None
        self.ioPlaced = None
        self.dcrRouted = None
        self.powerRouted = None
        self.routeStatus = None
        self.utilizationPlaced = None
        self.controlSetsPlaced = None
        self.timingSummaryRouted = None
        self.clokUtilizationRouted = None
        self.bitstreamFile = None

        # synth
        self.utilizationSynth = None

class XilinxPartBuilder():
    class Package():
        #zynq
        clg484 = "clg484"
        
        # all kintex7 packages
        fbv676 = "fbv676"
        fbv484 = "fbv484"
        fbg676 = "fbg676"
        fbg484 = "fbg484"
        ffg676 = "ffg676"
        ffv676 = "ffv676"
        ffg900 = "ffg900"
        ffv900 = "ffv900"
        fgb900 = "fgb900"
        fbg900 = "fbg900"
        ffv901 = "ffv901"
        ffg901 = "ffg901"
        ffv1156 = "ffv1156"
        ffg1156 = "ffg1156"
        rf676 = "rf676"
        rf900 = "rf900"
        
    class Size():
        #zynq sizes
        _010 = "010"
        _020 = "020"
        _030 = "030"
        _035 = "035"
        _040 = "040"
        
        _70t = "70t"
        _160t = "160t"
        _325t = "325t"
        _355t = "355t"
        _410t = "410t"
        _420t = "420t"
        _480t = "480t"
        # boundary between kintex 7 and virtex 7 
        _585t = "585t"
        _2000t = "2000t"
        h580 = "h580"
        h870 = "h870"
        x330 = "x330" 
        x415 = "x415"
        x485 = "x485"
        x550 = "x550"
        x680 = "x680"
        x690 = "x690"
        x1140 = "x1140" 
        
    class Family():
        zynq7000 = '7z'
        atrix7 = '7a'
        kintex7 = '7k'
        virtex7 = '7v'
        
    class Speedgrade():
        _1 = "-1"
        _2 = "-2"
        _3 = "-3"
        
    def __init__(self, family, size, package, speedgrade):
        self.family = family
        self.size = size
        self.package = package
        self.speedgrade = speedgrade
        
    def name(self):
        return "xc" + self.family + self.size + self.package + self.speedgrade

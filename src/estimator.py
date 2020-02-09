class Estimator:
    def __init__(self, configuration):
        self.appType = configuration["type"]
        if self.appType == "Matrix Multiplication":
            self.estimate_MM(configuration)
        else:
            print("App type " + self.appType + " not supported")
            exit(0)

    def estimate_MM(self, configuration):
        self.verbose = int(configuration["verbose"])
        assert self.verbose == 0 or self.verbose == 1 or self.verbose == 2
        self.rowDim = int(configuration["row"])
        self.columnDim = int(configuration["column"])
        self.PE = self.columnDim * self.rowDim
        self.inputRow = int(configuration["input row"])
        self.inputColumn = int(configuration["input column"])
        self.frequency = int(configuration["frequency"])

        if self.verbose == 0:
            self.logic = 3998 * self.PE + 8221
            self.shiftReg = 483 * self.PE + 260
            self.reg = 7547 * self.PE + 17184
            self.DSP = 40 * self.PE
            self.BRAM = 3.125 * self.PE + 140

        elif self.verbose == 1:
            self.logic = 3998 * self.PE + 8221
            self.shiftReg = 483 * self.PE + 260
            self.reg = int(configuration["register"])
            self.DSP = int(configuration["DSP"])
            self.BRAM = int(configuration["BRAM"])
        else:
            self.logic = int(configuration["logic"])
            self.shiftReg = int(configuration["shift register"])
            self.reg = int(configuration["register"])
            self.DSP = int(configuration["DSP"])
            self.BRAM = int(configuration["BRAM"])

        self.clockPower = self.estimate_MM_clock()

        self.logicPower = self.estimate_MM_logic()

        self.DSPPower = self.estimate_MM_DSP()

        self.BRAMPower = self.estimate_MM_BRAM()

    
    def estimate_MM_clock(self):
        """
        clock buffer enable rate: 100%
        slice buffer enable rate: 30%
        """
        fanout = self.shiftReg + self.reg + self.DSP + 2 * self.BRAM
        fanoutPerSite = -0.01381219949 * pow(self.PE, 1.5) + 0.207259816 * self.PE - 0.7502239272 * pow(self.PE, 0.5) + 3.189499138
        coifficient = -0.000001033189099 * fanoutPerSite  + 0.00003178538474 / pow(fanoutPerSite, 2) + 0.00001112569767
        return (self.frequency / 333.33333) * (coifficient * fanout + 0.245)
    
    def estimate_MM_logic(self):
        """
        based on #of each units
        toggle rate and complexity are set to default
        """
        return 0
    
    def estimate_MM_DSP(self):
        """

        """
        return 0
    
    def estimate_MM_BRAM(self):
        """
        """
        return 0

    def printResult(self):
        power = self.clockPower + self.logicPower + self.DSPPower + self.BRAMPower
        print(power)
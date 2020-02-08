class Estimator:
    def __init__(self, configuration):
        self.appType = configuration["type"]
        self.verbose = int(configuration["verbose"])
        self.rowDim = int(configuration["row"])
        self.columnDim = int(configuration["column"])
        self.inputRow = int(configuration["inputRow"])
        self.inputColumn = int(configuration["inputColumn"])

    def printResult(self):
        pass
class pulseConfiguration():
    def __init__(self):
        self.CountDuration = 0
        self.CountNumber = 0
        self.Threshold = 0
        self.AveragesNumber = 0
        self.StartPump = 0
        self.WidthPump = 0
        self.StartMW = 0
        self.WidthMW = 0
        self.StartImage = 0
        self.WidthImage = 0
        self.StartReadout = 0
        self.LaserLow = 0
        self.LaserHigh = 0
        self.RFPower = 0
        self.measurementType = None

    # def __init__(self, countDuration, countNumber, threshold, averagesNumber, 
    #                 startPump, widthPump, startMW, widthMW, startImage, widthImage, 
    #                 startReadout, laserLow, laserHigh):
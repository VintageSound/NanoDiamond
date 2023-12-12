class pulseConfiguration():
    def __init__(self):
        self.count_duration = 0
        self.count_number = 0
        self.threshold = 0
        self.iterations = 0
        self.pump_start = 0
        self.pump_duration = 0
        self.microwave_start = 0
        self.microwave_duration = 0
        self.image_start = 0
        self.image_duration = 0
        self.readout_start = 0
        self.low_voltage_AOM = 0
        self.high_voltage_AOM = 0
        self.microwave_power = 0
        self.measurement_type = None

    # def __init__(self, countDuration, countNumber, threshold, averagesNumber, 
    #                 startPump, widthPump, startMW, widthMW, startImage, widthImage, 
    #                 startReadout, laserLow, laserHigh):
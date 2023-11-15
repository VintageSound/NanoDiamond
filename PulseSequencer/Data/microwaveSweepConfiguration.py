
class microwaveSweepConfiguration:
    def __init__(self):
        self.centerFreq = 0
        self.power = 0
        self.powerSweepStart = 0
        self.powerSweepStop = 0
        self.startFreq = 0
        self.stopFreq = 0
        self.stepSize = 0
        self.stepTime = 0
        self.trigMode = 0

    def __init__(self, centerFreq, power, powerSweepStart, powerSweepStop, 
                    startFreq, stopFreq, stepSize, stepTime, trigMode):
        self.centerFreq = centerFreq
        self.power = power
        self.powerSweepStart = powerSweepStart
        self.powerSweepStop = powerSweepStop
        self.startFreq = startFreq
        self.stopFreq = stopFreq
        self.stepSize = stepSize
        self.stepTime = stepTime
        self.trigMode = trigMode

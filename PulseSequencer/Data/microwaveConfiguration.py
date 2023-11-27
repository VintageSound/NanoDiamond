
class microwaveConfiguration:
    def __init__(self, centerFreq = 0, power = 0, powerSweepStart = 0, powerSweepStop = 0,
                    startFreq = 0, stopFreq = 0, stepSize = 0, stepTime = 0, trigMode = 0):
        self.centerFreq = centerFreq
        self.power = power
        self.powerSweepStart = powerSweepStart
        self.powerSweepStop = powerSweepStop
        self.startFreq = startFreq
        self.stopFreq = stopFreq
        self.stepSize = stepSize
        self.stepTime = stepTime
        self.trigMode = trigMode

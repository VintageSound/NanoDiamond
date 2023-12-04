import time
import traceback
import pandas as pd
import numpy as np

from Data.measurementType import measurementType
from Data.repetition import repetition
from Data.pulseConfiguration import pulseConfiguration
from LogicManagers.measurementManager import measurementManager

class scanManager():
    def __init__(self, measurementManager: measurementManager) -> None:
        self.measurementManager = measurementManager
        self.timeRange = []
        self.currentIteration = 0
        self.config = None
        self.measurementData = {}
        pass

    def startRabiScanSequence(self, pulseConfig : pulseConfiguration, startTime, endTime, timeStep):
        self.config = pulseConfig
        self.timeRange = list(range(startTime, endTime, timeStep))
        self.currentIteration = 0
        self.config.WidthMW = self.timeRange[self.currentIteration] 

        self.measurementManager.registerToRabiPulseDataRecivedEvent(self.rabiPulseEndedEventHandler)
        self.measurementManager.startNewRabiPulseMeasuremnt(config=self.config)
        
    def rabiPulseEndedEventHandler(self, data):
        self.measurementData[self.config.WidthMW] = data
        
        # TODO: add calculation of rabi point 

    def continueCurrentScan(self):
        self.currentIteration += 1
        self.config.WidthMW = self.timeRange[self.currentIteration] 
        self.measurementManager.startNewRabiPulseMeasuremnt(config=self.config)
    

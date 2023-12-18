import time
import traceback
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

from Data.measurementType import measurementType
from Data.repetition import repetition
from Data.pulseConfiguration import pulseConfiguration
from LogicManagers.measurementManager import measurementManager
from LogicManagers import pulseAnalayzer 

class scanManager():
    def __init__(self, measurementManager: measurementManager) -> None:
        self.measurementManager = measurementManager
        self.timeRange = []
        self.extractedData = {}
        self.measurementData = {}

        self.currentIteration = 0
        self.normalizationFactor = 0

        self.timeColumn = self.measurementManager.RabiXAxisLabel
        self.valueColumn = self.measurementManager.RabiYAxisLabel

        self.pulseConfig = None
        self.microwaveConfig = None
        self.rabiPulseEndedEvent = []

        self.isMeasurementActive = False

    def registerToRabiPulseEndedEvent(self, callback):
        self.rabiPulseEndedEvent.append(callback)

    def raiseRabiPulseEndedEvent(self):
        for callback in self.rabiPulseEndedEvent:
            callback()

    def startRabiScanSequence(self, pulse_config : pulseConfiguration, microwave_config : pulseConfiguration, startTime, endTime, timeStep):
        self.pulseConfig = pulse_config
        self.microwaveConfig = microwave_config
        self.timeRange = list(range(startTime, endTime, timeStep))
        self.extractedData = {}
        self.measurementData = {}
        self.currentIteration = 0
        self.pulseConfig.microwave_duration = self.timeRange[self.currentIteration] 
        self.isMeasurementActive = True

        self.measurementManager.registerToRabiPulseDataRecivedEvent(self.rabiPulseEndedEventHandler)
        self.measurementManager.startNewRabiPulseMeasurement(pulseConfig = self.pulseConfig, microwaveConfig = self.microwaveConfig)
        
    def rabiPulseEndedEventHandler(self, data):
        self.measurementData[self.config.microwave_duration] = data
        self.rabiPulseEndedEvent(data, self.config.microwave_duration)
        newPoint = self.extractPointFromPulseSequence(data)

        self.measurementData[self.timeRange[self.currentIteration]] = data
        self.extractedData[self.timeRange[self.currentIteration]] = newPoint

        self.continueCurrentScan()

    # Dima Normalization. normalize the values by the integraion of the entire pump pulse
    def extractPointFromPulseSequence(self, pulseSequence : pd.DataFrame):
        if self.currentIteration == 0:
            self.setNormalizationFactor()

        # Because of the laser power drift it's necessary to make normalization.
        # For that just integrate first fluorescence pulse counts for each data file
        # and compare it with the same value but for first data file.
        # Their ratio gives you factor which you need just multiply by current data
        # and that's it, you implemented your normalization. You're amazing!    
        integration_pump = pulseAnalayzer.getIntegraionOfPump(pulseSequence[self.timeColumn], pulseSequence[self.valueColumn])
        normalized_data = pulseSequence[self.valueColumn] * (self.normalizationFactor / integration_pump)

        # Now you need to measure decrease in fluoresce signal of the second pulse at its beginning.
        # Eventually, it will show your desired Rabi oscillation.
        # For that just integrate second fluorescence pulse (at the beginning) for 0.5 msec.
        # Okay, it seems that now you got it! Just plot it.
        integration_image = pulseAnalayzer.getIntegraionOfImageBegining(normalized_data)

        return integration_image

    def setNormalizationFactor(self, pulseSequence : pd.DataFrame):
        self.normalizationFactor = pulseAnalayzer.getIntegraionOfPump(pulseSequence[self.timeColumn], pulseSequence[self.valueColumn])

    def continueCurrentScan(self):
        if not self.isMeasurementActive:
            return

        self.currentIteration += 1
        self.config.microwave_duration = self.timeRange[self.currentIteration] 
        self.measurementManager.startNewRabiPulseMeasurement(config=self.config)
    

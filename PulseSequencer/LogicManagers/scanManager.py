import time
import traceback
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal

from Data.measurementType import measurementType
from Data.repetition import repetition
from Data.pulseConfiguration import pulseConfiguration
from LogicManagers.measurementManager import measurementManager
from LogicManagers import pulseAnalayzer
from Data.microwaveConfiguration import microwaveConfiguration 

class scanManager(QObject):
    rabiPulseEndedEvent = pyqtSignal(float, float)
    errorEvent = pyqtSignal(Exception)

    def __init__(self, measurementManager: measurementManager) -> None:
        super().__init__()

        self.measurementManager = measurementManager
        self.timeRange = []
        self.extractedData_dima = {}
        self.extractedData_hezi = {}
        self.measurementData = {}

        self.currentIteration = 0
        self.normalizationFactor = 0

        self.timeColumn = self.measurementManager.RabiXAxisLabel
        self.valueColumn = self.measurementManager.RabiYAxisLabel

        self.pulseConfig = None
        self.microwaveConfig = None

        self.isMeasurementActive = False

    def startScanAsync(self, 
                pulse_config : pulseConfiguration, 
                microwave_config : microwaveConfiguration, 
                startTime, 
                endTime, 
                timeStep):
        self.scanWorker = ScanWorkerThread(self,
                                           pulse_config,
                                           microwave_config,
                                           startTime,
                                           endTime,
                                           timeStep)
        self.scanWorker.start()
        return self.scanWorker

    # Need to run this function as a for loop condition
    # for point, time in self.scanManager.startScan(...)
    #   print(point, time) ## Do Something with the data...
    def startScan(self, 
                pulse_config : pulseConfiguration, 
                microwave_config : microwaveConfiguration, 
                startTime, 
                endTime, 
                timeStep):
        self.normalizationFactor = 0
        self.pulseConfig = pulse_config
        self.microwaveConfig = microwave_config
        self.timeRange = np.arange(startTime, endTime, timeStep)
        self.extractedData_dima = {}
        self.measurementData = {}
        self.isMeasurementActive = True

        for time in self.timeRange:
            self.pulseConfig.microwave_duration = time
            data = self.measurementManager.startNewRabiPulseMeasurement(self.pulseConfig, self.microwaveConfig)
            self.measurementData[time] = data

            newPoint_dima = self.extractPointFromPulseSequence_Dima(data)
            newPoint_hezi = self.extractPointFromPulseSequence_Hezi(data)
            self.extractedData_dima[time] = newPoint_dima
            self.extractedData_hezi[time] = newPoint_hezi
            
            yield newPoint_dima, time

            if not self.isMeasurementActive:
                break
        
    # Dima Normalization. normalize the values by the integraion of the entire pump pulse
    def extractPointFromPulseSequence_Dima(self, pulseSequence : pd.DataFrame):
        if self.normalizationFactor == 0:
            self.setNormalizationFactor(pulseSequence)

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
        integration_image = pulseAnalayzer.getIntegraionOfImageBegining(pulseSequence[self.timeColumn], normalized_data)
        result = integration_image / self.normalizationFactor
        
        return result

    # Hezi Normalization. normalize the values by the last 300 ns of the image
    def extractPointFromPulseSequence_Hezi(self, pulseSequence : pd.DataFrame):
        time_image, data_image = pulseAnalayzer.getOnlyImage(pulseSequence[self.timeColumn], pulseSequence[self.valueColumn])
        time_label = "Time"
        data_label = "Data"
        start_time_image = time_image[0]
        end_time_image = time_image[-1]
        
        image_df = pd.DataFrame({time_label : time_image, data_label : data_image})
        peak = image_df[(image_df[time_label] > start_time_image) & (image_df[time_label] < (start_time_image + 0.3))]
        reference = image_df[(image_df[time_label] > (end_time_image - 0.3)) & (image_df[time_label] < end_time_image)]

        peak_integration = np.sum(peak[data_label])
        reference_integration = np.sum(reference[data_label])

        result = (peak_integration - reference_integration)/(peak_integration + reference_integration)

        return result

    def setNormalizationFactor(self, pulseSequence : pd.DataFrame):
        self.normalizationFactor = pulseAnalayzer.getIntegraionOfPump(pulseSequence[self.timeColumn], pulseSequence[self.valueColumn])

class ScanWorkerThread(QThread):
    def __init__(self, 
                 manager : scanManager,
                 pulse_config : pulseConfiguration, 
                 microwave_config : microwaveConfiguration, 
                 startTime, 
                 endTime, 
                 timeStep):
        super().__init__()

        self.scanManager = manager
        self.pulseConfig = pulse_config
        self.microwaveConfig = microwave_config
        self.startTime = startTime
        self.endTime = endTime
        self.timeStep = timeStep

    def run(self):
        try:
            for point, time in self.scanManager.startScan(self.pulseConfig, self.microwaveConfig, self.startTime, self.endTime, self.timeStep):
                self.scanManager.rabiPulseEndedEvent.emit(point, time)
        except Exception as ex:
            print("Error in ScanWorkerThread:", ex)
            self.scanManager.errorEvent.emit(ex)
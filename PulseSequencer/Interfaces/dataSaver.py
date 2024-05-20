
from datetime import datetime
import numpy as np
import pandas as pd
import os
from os import path
import csv

from Data.measurementType import measurementType
from LogicManagers.measurementManager import measurementManager
from LogicManagers.MeasurementProcessor import MeasurementProcessor
from LogicManagers.scanManager import scanManager
from Interfaces.redPitayaInterface import redPitayaInterface

class dataSaver():
    def __init__(self, measurmentManager : measurementManager = None, scanManager : scanManager = None, measurementProcessor: MeasurementProcessor = None):
        self.currentDate = datetime.date(datetime.now())
        self.measurmentManager = measurmentManager
        self.scanManager = scanManager
        self.measurementProcessor = measurementProcessor
        self.ODMRIndex = 0
        self.rabiIndex = 0
        self.scanIndex = 0

        self.basePath = path.join(r'D:\Experiments', str(self.currentDate))
        self.ODMRFolder = path.join(self.basePath, "ODMR")
        self.rabiFolder = path.join(self.basePath, "Pulse_Sequence")
        self.scanFolder = path.join(self.basePath, "Scans")

    def getODMRFolderToSave(self):
        return self.ODMRFolder

    def getRabiFolderToSave(self):
        return self.rabiFolder

    def getScansFolderToSave(self):
        return self.scanFolder

    def setODMRFolderToSave(self, newPath):
        self.ODMRFolder = path.realpath(newPath)    
        os.makedirs(self.ODMRFolder, exist_ok=True)

    def setRabiFolderToSave(self, newPath):
        self.rabiFolder = path.realpath(newPath)
        os.makedirs(self.rabiFolder, exist_ok=True)

    def saveODMR(self, comment, file_name= None):
        data = self.measurmentManager.ODMRData
        pulseConfig = self.measurmentManager.pulseConfigODMR
        number_of_iterations = self.measurmentManager.measurementCountODMR
        microwaveConfig = self.measurmentManager.microwaveODMRConfig

        if file_name is None:
            file_name = str(self.rabiIndex)

        metadata = {'Measurement type:': measurementType.ODMR.name,
                'RF Power [dBm]:': pulseConfig.microwave_power,
                'Measurment Duration [us]:': pulseConfig.count_duration * redPitayaInterface.timeStep,
                'Comment:': comment,
                'Scan Start Frequency [MHz]:': microwaveConfig.startFreq,
                'Scan Stop Frequency [MHz]:': microwaveConfig.stopFreq,
                'Number of Iterations:' : number_of_iterations}

        filePath = os.path.join(self.ODMRFolder, file_name + ".pkl")

        self.savePickle(filePath, metadata, data)
        self.ODMRIndex += 1

    def saveRabiPulse(self, comment, file_name = None):
        data = self.measurmentManager.RabiData
        pulseConfig = self.measurmentManager.pulseConfigRabi
        microwaveConfig = self.measurmentManager.microwaveRabiConfig

        if file_name is None:
            file_name = str(self.rabiIndex)

        metadata = {'Measurement type': pulseConfig.measurement_type.name,
                'RF Power [dBm]': pulseConfig.microwave_power,
                'Measurement Duration [us]': pulseConfig.count_duration,
                'Comment': comment,
                'MW frequency [MHz]': microwaveConfig.centerFreq,
                'Pump pulse time [us]': pulseConfig.pump_start,
                'Pump pulse duration [us]': pulseConfig.pump_duration,
                'MW pulse time [us]': pulseConfig.microwave_start,
                'MW pulse duration [us]': pulseConfig.microwave_duration,
                'Imaging pulse time [us]': pulseConfig.image_start,
                'Imaging Pulse duration [us]': pulseConfig.image_duration,
                'Readout pulse time [us]': pulseConfig.readout_start,
                'Averages Number': pulseConfig.iterations}
   
        filePath = os.path.join(self.rabiFolder, file_name + ".pkl")

        self.savePickle(filePath, metadata, data)
        self.rabiIndex += 1

    def saveCompleteScan(self, comment, file_name = None):
        full_data = self.scanManager.measurementData
        pulse_config = self.scanManager.pulseConfig        
        microwave_config = self.scanManager.microwaveConfig        

        if file_name is None:
            file_name = str(self.scanIndex)

        metadata = {'Measurement type': pulse_config.measurement_type.name,
                    'RF Power [dBm]': pulse_config.microwave_power,
                    'Measurement Duration [us]': pulse_config.count_duration,
                    'Comment': comment,
                    'MW frequency [MHz]': microwave_config.centerFreq,
                    'Pump pulse time [us]': pulse_config.pump_start,
                    'Pump pulse duration [us]': pulse_config.pump_duration,
                    'MW pulse time [us]': pulse_config.microwave_start,
                    'MW pulse duration [us]': pulse_config.microwave_duration,
                    'Imaging pulse time [us]': pulse_config.image_start,
                    'Imaging Pulse duration [us]': pulse_config.image_duration,
                    'Readout pulse time [us]': pulse_config.readout_start,
                    'Number of Iterations:': pulse_config.iterations}
   
        filePath = os.path.join(self.scanFolder, file_name + ".pkl")

        for time in full_data:
            data = full_data[time]
            metadata['MW pulse duration [us]'] = time
            self.savePickle(filePath, metadata, data)

        extractedPoints = pd.DataFrame({'Time' : self.scanManager.extractedData_dima.keys(),
                                        'Population' : self.scanManager.extractedData_dima.values()})
        self.savePickle(filePath, metadata, extractedPoints)

        self.scanIndex += 1

    def savePhotonsAVG(self, file_name = None):
        if file_name is None:
            file_name = str(self.rabiIndex)

        data = self.measurementProcessor.photonsAVGHistory
        metadata = {}

        filePath = os.path.join(self.ODMRFolder, file_name + "_photonsAVG.pkl")
        self.savePickle(filePath, metadata, data)

        filePath = os.path.join(self.ODMRFolder, file_name + "_photonsAVG.csv")
        self.saveCsv(filePath, data)

    def loadCompleteScan(self, filePath):
        metadadata_list = []
        data_list = []

        with open(filePath, 'rb') as fin:
            while True:
                try:
                    pdMetadata = pd.read_pickle(fin)
                    data = pd.read_pickle(fin)
                    metadadata_list.append(pdMetadata)
                    data_list.append(data)
                except EOFError:
                    break

        return metadadata_list, data_list

    def saveCsv(self, filePath, data):
        data.to_csv(filePath)
        print(filePath)

    def savePickle(self, filePath, metadata, data : pd.DataFrame):
        print(filePath)

        directory = path.dirname(filePath)
        os.makedirs(directory, exist_ok=True)
        pdMetadata = pd.Series(metadata)

        with open(filePath, 'ab') as fout:
            pdMetadata.to_pickle(fout)
            data.to_pickle(fout)

    def loadPickle(self, filePath):
        with open(filePath, 'rb') as fin:
            pdMetadata = pd.read_pickle(fin)
            data = pd.read_pickle(fin)

        return pdMetadata, data
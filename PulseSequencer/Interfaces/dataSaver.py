
from datetime import datetime
import numpy as np
import pandas as pd
import os
from os import path

from Data.measurementType import measurementType
from Interfaces.QRedPitayaInterface import QRedPitayaInterface
from LogicManagers.measurementManager import measurementManager
from LogicManagers.scanManager import scanManager

class dataSaver():
    def __init__(self, measurmentManager : measurementManager = None, scanManager : scanManager = None):
        self.currentDate = datetime.date(datetime.now())
        self.measurmentManager = measurmentManager
        self.scanManager = scanManager
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
                'Measurment Duration [us]:': pulseConfig.count_duration * QRedPitayaInterface.timeStep,
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

        metadata = {'Measurement type': measurementType.RabiPulse.name,
                'RF Power [dBm]': pulseConfig.microwave_power,
                'Measurement Duration [us]': pulseConfig.count_duration * QRedPitayaInterface.timeStep,
                'Comment': comment,
                'MW frequency [MHz]': microwaveConfig.centerFreq,
                'Pump pulse time [us]': pulseConfig.pump_start,
                'Pump pulse duration [us]': pulseConfig.pump_duration * QRedPitayaInterface.timeStep,
                'MW pulse time [us]': pulseConfig.microwave_start * QRedPitayaInterface.timeStep,
                'MW pulse duration [us]': pulseConfig.microwave_duration * QRedPitayaInterface.timeStep,
                'Imaging pulse time [us]': pulseConfig.image_start * QRedPitayaInterface.timeStep,
                'Imaging Pulse duration [us]': pulseConfig.image_duration * QRedPitayaInterface.timeStep,
                'Readout pulse time [us]': pulseConfig.readout_start * QRedPitayaInterface.timeStep,
                'Averages Number': pulseConfig.iterations}
   
        filePath = os.path.join(self.rabiFolder, file_name + ".pkl")

        self.savePickle(filePath, metadata, data)
        self.rabiIndex += 1

    def saveCompleteScan(self, comment, file_name = None):
        pass

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
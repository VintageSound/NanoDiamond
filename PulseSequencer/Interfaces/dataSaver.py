
from datetime import datetime
import numpy as np
import pandas as pd
import os
from os import path

from Data.measurementType import measurementType
from Interfaces.redPitayaInterface import redPitayaInterface
from LogicManagers.measurementManager import measurementManager

class dataSaver():
    def __init__(self, measurmentManager : measurementManager = None):
        self.currentDate = datetime.date(datetime.now())
        self.measurmentManager = measurmentManager
        self.ODMRIndex = 0
        self.rabiIndex = 0

        self.basePath = path.join(r'D:\Experiments', str(self.currentDate))
        self.ODMRFolder = path.join(self.basePath, "ODMR")
        self.rabiFolder = path.join(self.basePath, "Pulse_Sqeunce")
        self.scanFolder = path.join(self.basePath, "Scans")

    def getODMRFolderToSave(self):
        return self.ODMRFolder

    def getRabiFolderToSave(self):
        return self.rabiFolder

    def getScansFolderToSave(self):
        return self.scanFolder

    def setODMRFolderToSave(self, newPath):
        # # if path.realpath(newPath):
        # #     raise(Exception(newPath + " invalid path"))
        # os.makedirs(newPath)
        self.ODMRFolder = path.realpath(newPath)    

    def setRabiFolderToSave(self, newPath):
        # os.makedirs(newPath)
        self.rabiFolder = path.realpath(newPath)

    def saveODMR(self, comment):
        data = self.measurmentManager.ODMRData
        pulseConfig = self.measurmentManager.pulseConfigODMR
        number_of_iterations = self.measurmentManager.measurementCountODMR
        microwaveConfig = self.measurmentManager.microwaveODMRConfig

        metadata = {'Measurement type:': measurementType.ODMR.name,
                'RF Power [dBm]:': pulseConfig.microwave_power,
                'Measurment Duration [us]:': pulseConfig.count_duration * redPitayaInterface.timeStep,
                'Comment:': comment,
                'Scan Start Frequency [MHz]:': microwaveConfig.startFreq,
                'Scan Stop Frequency [MHz]:': microwaveConfig.stopFreq,
                'Number of Iterations:' : number_of_iterations}

        filePath = os.path.join(self.ODMRFolder, str(self.ODMRIndex) + ".pkl")

        self.savePickle(filePath, metadata, data)
        self.ODMRIndex += 1

    def saveRabiPulse(self, comment):
        data = self.measurmentManager.RabiData
        pulseConfig = self.measurmentManager.pulseConfigRabi
        microwaveConfig = self.measurmentManager.microwaveRabiConfig

        metadata = {'Measurement type': measurementType.RabiPulse.name,
                'RF Power [dBm]': pulseConfig.microwave_power,
                'Measurement Duration [us]': pulseConfig.count_duration * redPitayaInterface.timeStep,
                'Comment': comment,
                'MW frequency [MHz]': microwaveConfig.centerFreq,
                'Pump pulse time [us]': pulseConfig.pump_start,
                'Pump pulse duration [us]': pulseConfig.pump_duration * redPitayaInterface.timeStep,
                'MW pulse time [us]': pulseConfig.microwave_start * redPitayaInterface.timeStep,
                'MW pulse duration [us]': pulseConfig.microwave_duration * redPitayaInterface.timeStep,
                'Imaging pulse time [us]': pulseConfig.image_start * redPitayaInterface.timeStep,
                'Imaging Pulse duration [us]': pulseConfig.image_duration * redPitayaInterface.timeStep,
                'Readout pulse time [us]': pulseConfig.readout_start * redPitayaInterface.timeStep,
                'Averages Number': pulseConfig.iterations}
   
        filePath = os.path.join(self.rabiFolder, str(self.rabiIndex) + ".pkl")

        self.savePickle(filePath, metadata, data)
        self.rabiIndex += 1

    def savePickle(self, filePath, metadata, data : pd.DataFrame):
        print(filePath)

        directory = path.dirname(filePath)
        os.makedirs(directory, exist_ok=True)
        pdMetadata = pd.Series(metadata)

        with open(filePath, 'wb') as fout:
            pdMetadata.to_pickle(fout)
        # TODO: Check if needed:
        # with open(filePath, 'ab') as fout:
            data.to_pickle(fout)

def loadPickle(filePath):
    with open(filePath, 'rb') as fin:
        pdMetadata = pd.read_pickle(fin)
        data = pd.read_pickle(fin)

    return pdMetadata, data
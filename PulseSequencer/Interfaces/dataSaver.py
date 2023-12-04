
from datetime import datetime
import numpy as np
import pandas as pd
import os
from os import path

from Data.measurementType import measurementType
from Interfaces.redPitayaInterface import redPitayaInterface

class dataSaver():
    def __init__(self) -> None:
        self.currentDate = datetime.date(datetime.now())
        self.ODMRIndex = 0
        self.rabiIndex = 0

        self.basePath = path.join(r'D:/Experiments', str(self.currentDate))
        self.ODMRFolder = path.join(self.basePath, "ODMR")
        self.rabiFolder = path.join(self.basePath, "Rabi")

    def getODMRFolderToSave(self):
        return self.ODMRFolder

    def getRabiFolderToSave(self):
        return self.rabiFolder

    def setODMRFolderToSave(self, newPath):
        if path.realpath(newPath):
            raise(Exception(newPath + " invalid path"))
        
        self.ODMRFolder = newPath    

    def setRabiFolderToSave(self, newPath):
        if path.realpath(newPath):
            raise(Exception(newPath + " invalid path"))
        
        self.rabiFolder = newPath

    def saveODMR(self, data, pulseConfig, comment):
        metadata = {'Measurement type:': measurementType.ODMR.name,
                'RF Power [dBm]:': pulseConfig.RFPower,
                'Measurment Duration [us]:': pulseConfig.CountDuration * redPitayaInterface.timeStep,
                'Comment:': comment,
                'Scan Start Frequency [MHz]:': pulseConfig.startFreq,
                'Scan Stop Frequency [MHz]:': pulseConfig.stopFreq}

        filePath = os.path.join(self.ODMRFolder, str(self.ODMRIndex) + ".pkl")

        self.save(filePath, filePath, metadata, data)
        self.ODMRIndex += 1

    def saveRabi(self, data, pulseConfig, comment):
        metadata = {'Measurement type': measurementType.RabiPulse.name,
                'RF Power [dBm]': pulseConfig.RFPower,
                'Measurement Duration [us]': pulseConfig.CountDuration * redPitayaInterface.timeStep,
                'Comment': comment,
                'MW frequency [MHz]': pulseConfig.CenterFreq,
                'Pump pulse time [us]': pulseConfig.StartPump,
                'Pump pulse duration [us]': pulseConfig.WidthPump * redPitayaInterface.timeStep,
                'MW pulse time [us]': pulseConfig.StartMW * redPitayaInterface.timeStep,
                'MW pulse duration [us]': pulseConfig.WidthMW * redPitayaInterface.timeStep,
                'Imaging pulse time [us]': pulseConfig.StartImage * redPitayaInterface.timeStep,
                'Imaging Pulse duration [us]': pulseConfig.WidthImage * redPitayaInterface.timeStep,
                'Readout pulse time [us]': pulseConfig.StartReadout * redPitayaInterface.timeStep,
                'Averages Number': pulseConfig.AveragesNumber}
   
        filePath = os.path.join(self.rabiFolder, str(self.rabiFolder) + ".pkl")

        self.savePickle(filePath, filePath, metadata, data)
        self.rabiIndex += 1

    def savePickle(self, filePath, metadata, data : pd.DataFrame):
        print(filePath)

        directory = path.dirname(filePath)
        os.makedirs(directory, exist_ok=True)
        pdMetadata = pd.Series(metadata)

        with open(filePath, 'w') as fout:
            pdMetadata.to_pickle(fout)
            data.to_pickle(fout)
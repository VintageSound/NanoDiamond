
from datetime import datetime
import numpy as np
import pandas as pd
import os

from Data.MeasurementType import MeasurementType
from Interfaces.redPitayaInterface import redPitayaInterface

class dataSaver():
    def __init__(self) -> None:
        self.currentDate = datetime.date(datetime.now())
        pass

    def getFolderToSave(self):
        return r'D:/Experiments/' + str(self.currentDate) + r'/'

    def saveODMR(self):
        metadata = {'Measurement type:': MeasurementType.ODMR.name,
                'RF Power [dBm]:': self.pulseConfig.RFPower,
                'Measurment Duration [us]:': self.pulseConfig.CountDuration * redPitayaInterface.timeStep,
                'Comment:': self.txtComment.text(),
                'Param. value:': self.txtParamValue.text(),
                'Scan Start Frequency [MHz]:': self.sweepConfig.startFreq,
                'Scan Stop Frequency [MHz]:': self.sweepConfig.stopFreq}

        filePath = self.createFilePath()
        self.save(filePath, metadata, self.ODMRData)

    def saveRabi(self, pulseConfig, comment, paramValue):
        metadata = {'Measurement type': MeasurementType.Rabi.name,
                'RF Power [dBm]': pulseConfig.RFPower,
                'Measurement Duration [us]': pulseConfig.CountDuration * redPitayaInterface.timeStep,
                'Comment': comment,
                'Param. value': paramValue,
                'MW frequency [MHz]': pulseConfig.CenterFreq,
                'Pump pulse time [us]': pulseConfig.StartPump,
                'Pump pulse duration [us]': pulseConfig.WidthPump * redPitayaInterface.timeStep,
                'MW pulse time [us]': pulseConfig.StartMW * redPitayaInterface.timeStep,
                'MW pulse duration [us]': pulseConfig.WidthMW * redPitayaInterface.timeStep,
                'Imaging pulse time [us]': pulseConfig.StartImage * redPitayaInterface.timeStep,
                'Imaging Pulse duration [us]': pulseConfig.WidthImage * redPitayaInterface.timeStep,
                'Readout pulse time [us]': pulseConfig.StartReadout * redPitayaInterface.timeStep,
                'Averages Number': pulseConfig.AveragesNumber}

        filePath = self.createFilePath()
        self.save(filePath, metadata, self.RabiData)

    # TODO: comeplete
    def createFilePathODMR(self, textPath):
        filePath = self.txtPath.text() + r'/' + MeasurementType.ODMR.name + '_' + self.txtNum.text() + '.csv'
        return filePath

    # TODO: comeplete
    def createFilePathODMR(self, textPath):
        filePath = self.txtPath.text() + r'/' + MeasurementType.Rabi.name + '_' + self.txtNum.text() + '.csv'
        return filePath

    # TODO: change to pickle
    def save(self, filePath, metadata, data : pd.DataFrame):
        print(filePath)
        directory = os.path.dirname(filePath)
        os.makedirs(directory, exist_ok=True)
        pdMetadata = pd.Series(metadata)

        with open(filePath, 'w') as fout:
            pdMetadata.to_csv(fout)
            data.to_csv(fout)
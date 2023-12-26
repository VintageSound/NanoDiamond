import time
import traceback
import pandas as pd
import numpy as np
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal

from Data.pulseConfiguration import pulseConfiguration
from Data.microwaveConfiguration import microwaveConfiguration

from Interfaces.redPitayaInterface import redPitayaInterface
from Interfaces.pulseBlasterInterface import pulseBlasterInterface
from Interfaces.microwaveInterfaceSMR20 import microwaveInterfaceSMR20
from Interfaces.microwaveInterfaceWindFreak import microwaveInterfaceWindFreak
from Data.measurementType import measurementType
from Data.repetition import repetition

class measurementManager(QObject):
     # Events 
    AOMStatusChangedEvent = pyqtSignal()
    microwaveStatusChangeEvent = pyqtSignal()
    ODMRDataRecivedEvent = pyqtSignal(pd.DataFrame, int)
    rabiPulseDataRecivedEvent = pyqtSignal(pd.DataFrame)
    connectionErrorEvent = pyqtSignal(Exception)

    # Consts
    redPitayaTimeStep = redPitayaInterface.timeStep

    def __init__(self) -> None:
        super().__init__()

        # interfaces
        self.redPitaya = redPitayaInterface()
        self.pulseBlaster = pulseBlasterInterface()

        # Choose the correct microwave device
        # self.microwaveDevice = microwaveInterfaceWindFreak()
        self.microwaveDevice = microwaveInterfaceSMR20()

        # Column Names
        self.ODMRXAxisLabel = self.redPitaya.ODMRXAxisLabel
        self.ODMRYAxisLabel = self.redPitaya.ODMRYAxisLabel
        self.RabiXAxisLabel = self.redPitaya.RabiXAxisLabel 
        self.RabiYAxisLabel = self.redPitaya.RabiYAxisLabel

        # ODMR data
        self.pulseConfigODMR = pulseConfiguration()
        self.microwaveODMRConfig = microwaveConfiguration()
        self.HaveODMRData = False
        self.ODMRData = None
        self.measurementCountODMR = 0
        self.initializeODMRData()

        # Rabi data
        self.pulseConfigRabi = pulseConfiguration()
        self.microwaveRabiConfig = microwaveConfiguration()
        self.HaveRabiData = False
        self.RabiData = None
        self.measurementCountRabi = 0
        self.initializeRabiData()

        # setting variables
        self.measurementType = measurementType.ODMR
        self.repetition = repetition.RepeatAndSum
        self.isMeasurementActive = False

        self.range = []
        self.maxRepetitions = None

        # Events
        self.connectionErrorEvent.connect(self.handelConnectionError)

    # Data Methods
    def initializeODMRData(self):
        self.HaveODMRData = False
        self.measurementCountODMR = 0
        self.ODMRData = pd.DataFrame(0, index=np.arange(1024), columns=[self.ODMRXAxisLabel, self.ODMRYAxisLabel])

    def initializeRabiData(self):
        self.HaveRabiData = False
        self.RabiData = pd.DataFrame(0, index=np.arange(1024), columns=[self.RabiXAxisLabel, self.RabiYAxisLabel])

    def updateMicrowaveODMRConfig(self, config : microwaveConfiguration):
        self.microwaveODMRConfig = config
        self.microwaveDevice.sendODMRSweepCommand(self.microwaveODMRConfig)
    
    def updateMicrowaveRabiConfig(self, config : microwaveConfiguration):
        self.microwaveRabiConfig = config
        self.microwaveDevice.sendRabiCommand(self.microwaveRabiConfig)

    # Getters
    def getHaveODMRData(self):
        return self.HaveODMRData

    def getHaveRabiData(self):
        return self.HaveRabiData

    def getCurrentPulseConfig(self):
        if self.measurementType == measurementType.ODMR:
            return self.pulseConfigODMR
        
        if self.measurementType == measurementType.RabiPulse:
            return self.pulseConfigRabi

    def getODMRData(self):
        return self.ODMRData

    def getRabiData(self):
        return self.RabiData

    def getMeasurementType(self):
        return self.measurementType

    def getIsPulseBlasterConnected(self):
        return self.pulseBlaster.isConnected

    def connectToEverything(self):
        self.redPitaya.connect()
        self.pulseBlaster.connect()
        self.microwaveDevice.connect()

    def laserOpenCloseToggle(self, newConfig : pulseConfiguration):
        if self.redPitaya.isAOMOpen:
            self.redPitaya.closeAOM()
        else:
            if newConfig.measurement_type == measurementType.ODMR:
                self.pulseConfigODMR = newConfig
            elif newConfig.measurement_type == measurementType.RabiPulse: 
                self.pulseConfigRabi = newConfig

            self.redPitaya.congifurePulse(newConfig)
            self.redPitaya.openAOM()

        self.AOMStatusChangedEvent.emit()

    def pulseBlasterConnectionToggle(self, ip = None, port = None):
        if self.pulseBlaster.isConnected:
            self.disconnectFromPulseBlaster()
        else:
            self.connectToPulseBlaster(ip, port)

    def connectToPulseBlaster(self, ip = None, port = None):
        if not self.pulseBlaster.isConnected:
            self.pulseBlaster.connect(ip, port)

    def disconnectFromPulseBlaster(self):
        if self.pulseBlaster.isConnected:
            self.pulseBlaster.disconnect()

    def microwaveDeviceConnectionToggle(self):
        if self.microwaveDevice.getIsConnected():
            self.microwaveDevice.disconnect()
        else:
            self.microwaveDevice.connect()

        self.microwaveStatusChangeEvent.emit()

    def microwaveOnOffToggle(self):
        if not self.getIsMicrowaveConnected():
            raise Exception('Trying to send command to disconnected microwave device!')

        if self.getIsMicrowaveOn():
            self.microwaveDevice.turnOffMicrowave()
        else:
            self.microwaveDevice.turnOnMicrowave()

        self.microwaveStatusChangeEvent.emit()

    def connectToRedPitayaToggle(self, ip=None, port=None):
        if (ip is not None) and (port is not None):
            self.redPitaya.updateIpAndPort(ip, port)

        if self.getIsRedPitayaConnected():
            self.redPitaya.disconnect()
        else:
            self.redPitaya.connect()

    def configurePulseSequenceForODMR(self, config=None):
        if config is not None:
            self.pulseConfigODMR = config

        self.pulseConfigODMR.measurement_type = measurementType.ODMR

        self.redPitaya.congifurePulse(self.pulseConfigODMR)
        self.pulseBlaster.configurePulseBlaster(self.pulseConfigODMR)

    def configurePulseSequenceForRabi(self, config=None):
        if config is not None:
            self.pulseConfigRabi = config

        self.pulseConfigRabi.measurement_type = measurementType.RabiPulse

        self.redPitaya.congifurePulse(self.pulseConfigRabi)
        self.pulseBlaster.configurePulseBlaster(self.pulseConfigRabi)

    # Status Methods
    def getIsRedPitayaConnected(self):
        return self.redPitaya.getIsConnectionOpen()

    def getIsLaserOpen(self):
        return self.redPitaya.isAOMOpen

    def getIsMicrowaveConnected(self):
        return self.microwaveDevice.getIsConnected()

    def getIsMicrowaveOn(self):
        return self.microwaveDevice.checkIfMicrowaveIsOn()

    # Measurement Methods
    def _ODMRMeasurement(self):
        while self.isMeasurementActive:
            data = self.redPitaya.startODMR(self.pulseConfigODMR, self.microwaveODMRConfig, self.isMeasurementActive)

            self.saveODMRDataToDataFrame(data)
            self.measurementCountODMR += 1
            self.ODMRDataRecivedEvent.emit(self.ODMRData, self.measurementCountODMR)
            self.updateIsMeasurementActive()

        return self.ODMRData

    def updateIsMeasurementActive(self):
        if not self.isMeasurementActive:
            return 

        if (self.measurementType != measurementType.ODMR or
                self.repetition == repetition.Single):
            self.isMeasurementActive = False
            return 

        if (self.maxRepetitions is not None and
                self.measurementCountODMR >= self.maxRepetitions):
            self.isMeasurementActive = False
            return

    def _RabiPulseMeasurement(self):
        data = self.redPitaya.startRabiMeasurement(self.isMeasurementActive)

        self.saveRabiDataToDataFrame(data)
        self.rabiPulseDataRecivedEvent.emit(self.RabiData)

        return self.RabiData

    def startNewRabiPulseMeasurement(self, 
                                     pulseConfig : pulseConfiguration = None, 
                                     micrwaveConfig : microwaveConfiguration = None):
        if pulseConfig is not None:
            self.pulseConfigRabi = pulseConfig

        if micrwaveConfig is not None:
            self.microwaveRabiConfig = micrwaveConfig

        self.measurementType = pulseConfig.measurement_type
        self.isMeasurementActive = True
        self.initializeRabiData()
        self.configurePulseSequenceForRabi(self.pulseConfigRabi)
        self.updateMicrowaveRabiConfig(self.microwaveRabiConfig)

        self.redPitaya.closeAOM()
        self.AOMStatusChangedEvent.emit()
        
        self.microwaveDevice.turnOffMicrowave()
        self.microwaveStatusChangeEvent.emit()

        return self._RabiPulseMeasurement()

    def startNewODMRMeasurement(self,
                                pulseConfig : pulseConfiguration = None,
                                micrwaveConfig : microwaveConfiguration = None,
                                repeat=repetition.RepeatAndSum,
                                maxRepetitions=None):
        self.repetition = repeat
        self.maxRepetitions = maxRepetitions

        if micrwaveConfig is not None:
            self.microwaveODMRConfig = micrwaveConfig

        if pulseConfig is not None:
            self.pulseConfigODMR = pulseConfig

        self.measurementCountODMR = 0
        self.measurementType = measurementType.ODMR
        self.isMeasurementActive = True
        self.initializeODMRData()
        self.configurePulseSequenceForODMR(self.pulseConfigODMR)
        self.updateMicrowaveODMRConfig(self.microwaveODMRConfig)
        
        self.microwaveDevice.turnOnMicrowave()
        self.microwaveStatusChangeEvent.emit()

        self.redPitaya.openAOM()
        self.AOMStatusChangedEvent.emit()

        return self._ODMRMeasurement()

    def stopCurrentMeasurement(self):
        self.isMeasurementActive = False

    # Asyc Functions
    def startNewODMRMeasurementAsync(self,
                                    pulseConfig : pulseConfiguration = None,
                                    micrwaveConfig : microwaveConfiguration = None,
                                    repeat=repetition.RepeatAndSum,
                                    maxRepetitions=None):
        self.ODMRWorker = ODMRWorkerThread(self, pulseConfig, micrwaveConfig, repeat, maxRepetitions)
        self.ODMRWorker.start()
        return self.ODMRWorker

    def startNewRabiPulseMeasurementAsync(self, 
                                         pulseConfig : pulseConfiguration = None, 
                                         micrwaveConfig : microwaveConfiguration = None):
        self.rabiWorker = RabiWorkerThread(self,pulseConfig, micrwaveConfig)
        self.rabiWorker.start()
        return self.rabiWorker

    # Data Convertion
    def saveODMRDataToDataFrame(self, data):
        # Add the recived data to the stored data if needed
        if self.repetition == repetition.RepeatAndSum:
            self.ODMRData = self.sumTwoDataframes(self.ODMRData, data)
        else:
            self.ODMRData = data
        self.HaveODMRData = True
    
    def sumTwoDataframes(self, df1, df2):
        # Sum the two y columns and create a new dataframe
        df_sum = pd.DataFrame({df2.columns[0]: df2.iloc[:, 0], df2.columns[1]: df1.iloc[:, 1] + df2.iloc[:, 1]})
        
        return df_sum

    def saveRabiDataToDataFrame(self, data):
        self.RabiData = data
        self.HaveRabiData = True

    # Event Handlers
    def handelConnectionError(self, exception):
        self.redPitaya.reconnect()

class RabiWorkerThread(QThread):
    def __init__(self, 
                manager : measurementManager,
                pulseConfig : pulseConfiguration = None,
                micrwaveConfig : microwaveConfiguration = None):
        super().__init__()

        self.measurementManager = manager
        self.error = pyqtSignal(Exception)
        self.pulseConfig = pulseConfig
        self.microwaveConfig = micrwaveConfig

    def run(self):
        try:
            self.measurementManager.startNewRabiPulseMeasurement(self.pulseConfig,
                                                                 self.microwaveConfig)
        except Exception as ex:
            print("Ereror in RabiWorkerThread:",ex)
            self.measurementManager.connectionErrorEvent.emit(ex)
    
class ODMRWorkerThread(QThread):
    def __init__(self, 
                manager : measurementManager,
                pulseConfig : pulseConfiguration = None,
                micrwaveConfig : microwaveConfiguration = None,
                repeat = repetition.RepeatAndSum,
                maxRepetitions = None):
        super().__init__()

        self.measurementManager = manager
        self.pulseConfig = pulseConfig
        self.microwaveConfig = micrwaveConfig
        self.repeat = repeat
        self.maxRepetitions = maxRepetitions

    def run(self):
        try:
            self.measurementManager.startNewODMRMeasurement(self.pulseConfig,
                                                            self.microwaveConfig,
                                                            self.repeat,
                                                            self.maxRepetitions)
        except Exception as ex:
            print("Error in ODMRWorkerThread:", ex)
            self.measurementManager.connectionErrorEvent.emit(ex)
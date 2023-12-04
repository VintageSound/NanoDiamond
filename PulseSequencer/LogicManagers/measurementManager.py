import time
import traceback
import pandas as pd
import numpy as np

from Data.pulseConfiguration import pulseConfiguration
from Data.microwaveConfiguration import microwaveConfiguration

from Interfaces.redPitayaInterface import redPitayaInterface
from Interfaces.pulseBlasterInterface import pulseBlasterInterface
from Interfaces.microwaveInterface import microwaveInterface
from Interfaces.dataSaver import dataSaver
from Data.measurementType import measurementType
from Data.repetition import repetition


class measurementManager():
    maxPower = 2 ** 13  # not sure why...
    redPitayaTimeStep = redPitayaInterface.timeStep

    def __init__(self, QMainObject) -> None:
        # interfaces
        self.redPitaya = redPitayaInterface(QMainObject)
        self.pulseBaster = pulseBlasterInterface()
        self.microwaveDevice = microwaveInterface()

        # register Events:
        self.redPitaya.registerReciveData(self.receiveDataHandler)
        self.redPitaya.registerRedPitayaConnected(self.redPitayaConnectedHandler)
        self.redPitaya.registerConnectionError(self.receiveRedPitayaConnectionError)

        # ODMR data
        self.microwaveConfig = microwaveConfiguration()
        self.HaveODMRData = False
        self.ODMRXAxisLabel = "Frequency [MHz]"
        self.ODMRYAxisLabel = "Photons Counted"
        self.ODMRData = None
        self.measurementCountODMR = 0
        self.initializeODMRData()

        # Rabi data
        self.pulseConfig = pulseConfiguration()
        self.HaveRabiData = False
        self.RabiXAxisLabel = "Time [micro seconds]"
        self.RabiYAxisLabel = "Photons Counted"
        self.RabiData = None
        self.measurementCountRabi = 0
        self.initializeRabiData()

        # setting variables
        self.measurementType = measurementType.ODMR
        self.repetition = repetition.RepeatAndSum
        self.isMeasurementActive = False

        self.range = []
        self.repeatMeasurement = True

        self.maxRepetitions = None
        self.timeStep = 0
        self.size = 2048  # number of samples to show on the plot # max size
        self.initializeBufferODMR()

        # Events 
        self.AOMStatusChangedEvent = []
        self.redPitayaConnectedEvent = []
        self.ODMRDataRecivedEvent = []
        self.rabiPulseDataRecivedEvent = []
        self.connectionErrorEvent = []

    # Data Methods
    def initializeBufferODMR(self):
        self.size = 2048
        self.redPitaya.initalizeBuffer(self.size * 4)  # not sure why 4...
        self.initializeODMRData()

    def initializeBufferRabi(self):
        self.size = 1024
        self.redPitaya.initalizeBuffer(self.size * 4)  # not sure why 4...
        self.initializeRabiData()

    def initializeODMRData(self):
        self.HaveODMRData = False
        self.measurementCountODMR = 0
        self.ODMRData = pd.DataFrame(0, index=np.arange(1024), columns=[self.ODMRXAxisLabel, self.ODMRYAxisLabel])

    def initializeRabiData(self):
        self.HaveRabiData = False
        self.measurementCountRabi = 0
        self.RabiData = pd.DataFrame(0, index=np.arange(1024), columns=[self.RabiXAxisLabel, self.RabiYAxisLabel])

    def updateMicrowaveSweepConfig(self, config=None):
        if config is not None:
            self.microwaveConfig = config
        self.microwaveDevice.sendSweepCommand(self.microwaveConfig)

    # Getters
    def getHaveODMRData(self):
        return self.HaveODMRData

    def getHaveRabiData(self):
        return self.HaveRabiData

    def getODMRData(self):
        return self.ODMRData

    def getRabiData(self):
        return self.RabiData

    def getMeasurementType(self):
        return self.measurementType

    # Connection Methods
    def laserOpenCloseToggle(self):
        if self.redPitaya.isAOMOpen:
            self.redPitaya.closeAOM()
        else:
            self.redPitaya.congifurePulse(self.pulseConfig)
            self.redPitaya.openAOM()

        self.raiseAOMStatusChangedEvent()

    def connectToPulseBlaster(self):
        if not self.pulseBaster.isOpen:
            self.pulseBaster.connect()
            self.pulseBaster.configurePulseBlaster(self.pulseConfig)

    def microwaveDeviceConnectionToggle(self, config=None):
        if config is not None:
            self.microwaveConfig = config

        if self.microwaveDevice.getIsConnected():
            self.microwaveDevice.disconnect()
        else:
            self.microwaveDevice.connect()
            self.updateMicrowaveSweepConfig()

    def microwaveOnOffToggle(self):
        if not self.getIsMicrowaveConnected():
            raise Exception('Trying to send command to disconnected microwave device!')

        if self.getIsMicrowaveOn():
            self.microwaveDevice.turnOffMicrowave()
        else:
            self.microwaveDevice.turnOnMicrowave()

    def connectToRedPitayaToggle(self, ip=None, port=None):
        if (ip is not None) and (port is not None):
            self.redPitaya.updateIpAndPort(ip, port)

        if self.getIsRedPitayaConnected():
            self.redPitaya.disconnect()
        else:
            self.redPitaya.connect()

    def configurePulseSequence(self, config=None):
        if config is not None:
            self.pulseConfig = config

        self.redPitaya.congifurePulse(self.pulseConfig)
        self.pulseBaster.configurePulseBlaster(self.pulseConfig)

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
    def _ODMMeasurement(self):
        self.redPitaya.startODMR(self.pulseConfig)

    def _RabiPulseMeasurement(self):
        self.redPitaya.startRabiMeasurement(self.pulseConfig)

    def startNewRabiPulseMeasurement(self, config=None):
        self.measurementType = measurementType.RabiPulse
        self.isMeasurementActive = True
        self.initializeBufferRabi()
        self.configurePulseSequence(config)

        self.redPitaya.closeAOM()
        self.raiseAOMStatusChangedEvent()

        self._RabiPulseMeasurement()

    def startNewODMRMeasuremnt(self, repet=repetition.RepeatAndSum, config=None, maxRepetitions=None):
        self.repetition = repet
        self.maxRepetitions = maxRepetitions
        self.measurementCountODMR = 0

        self.measurementType = measurementType.ODMR
        self.isMeasurementActive = True
        self.initializeBufferODMR()
        self.configurePulseSequence(config)

        self._ODMMeasurement()

    def stopCurrentMeasurement(self):
        self.isMeasurementActive = False

    # Data Convertion
    def saveODMRDataToDataFrame(self, data):
        xData = np.linspace(self.microwaveConfig.startFreq, self.microwaveConfig.stopFreq, int(self.size / 2))
        yData = data

        # Add the recived data to the stored data if needed
        if self.repetition == repetition.RepeatAndSum:
            yData = self.ODMRData[self.ODMRYAxisLabel].tolist() + data

        self.ODMRData = pd.DataFrame({self.ODMRXAxisLabel: xData, self.ODMRYAxisLabel: yData})
        self.HaveODMRData = True

    def saveRabiDataToDataFrame(self, data):
        dataToPlot = np.array(data[0:int(self.size)], dtype=float)

        # check if Time step is the right constant...
        self.timeStep = self.pulseConfig.CountDuration / 1000 * self.pulseConfig.CountNumber / 100  # ???
        xData = np.linspace(0, int(self.size) * self.timeStep, int(self.size))
        yData = self.RabiData[self.RabiYAxisLabel].tolist() + dataToPlot

        print("yData", yData)

        self.RabiData = pd.DataFrame({self.RabiXAxisLabel: xData, self.RabiYAxisLabel: yData})
        self.HaveRabiData = True

    # Register Events
    def registerToAOMStatusChangedEvent(self, callback):
        self.AOMStatusChangedEvent.append(callback)

    def registerToRedPitayaConnectedEvent(self, callback):
        self.redPitayaConnectedEvent.append(callback)

    def registerToODMRDataRecivedEvent(self, callback):
        self.ODMRDataRecivedEvent.append(callback)

    def registerToRabiPulseDataRecivedEvent(self, callback):
        self.rabiPulseDataRecivedEvent.append(callback)

    def registerConnectionErrorEvent(self, callback):
        self.connectionErrorEvent.append(callback)

    # Raise Events
    def raiseAOMStatusChangedEvent(self):
        for callback in self.AOMStatusChangedEvent:
            callback()

    def raiseRedPitayaConnectedEvent(self):
        for callback in self.redPitayaConnectedEvent:
            callback()

    def raiseConnectionErrorEvent(self, error):
        for callback in self.connectionErrorEvent:
            callback()

    def raiseODMRDataRecivedEvent(self):
        if not self.HaveODMRData:
            return

        for callback in self.ODMRDataRecivedEvent:
            callback(self.ODMRData, self.measurementCountODMR)

    def raiseRabiDataRecivedEvent(self):
        if not self.HaveRabiData:
            return

        for callback in self.rabiPulseDataRecivedEvent:
            callback(self.RabiData)

    # Event Handlers    
    def redPitayaConnectedHandler(self):
        try:
            self.configurePulseSequence(self.pulseConfig)
            self.raiseRedPitayaConnectedEvent()

            # Take another measurement if needed
            self.continueCurrentMeasurement()

        except Exception:
            traceback.print_exc()

    def continueCurrentMeasurement(self):
        if not self.isMeasurementActive:
            return

        print("self.measurementType != measurementType.ODMR", self.measurementType != measurementType.ODMR)

        if (self.measurementType != measurementType.ODMR or
                self.repetition == repetition.Single):
            self.isMeasurementActive = False
            return

        if (self.maxRepetitions is not None and
                self.measurementCountODMR >= self.maxRepetitions):
            self.isMeasurementActive = False
            return

        # ----- delay loop -------
        time.sleep(0.5)
        # ------------------------
        self._ODMMeasurement()

        # TODO: check if needed?
        # elif self.measurementType == measurementType.RabiPulse:
        #     self._RabiMeasurement()

    def receiveDataHandler(self, data):
        try:
            if self.measurementType == measurementType.ODMR:
                converted_data = self.redPitaya.convertODMRData(data, self.size)
                self.saveODMRDataToDataFrame(converted_data)
                self.measurementCountODMR += 1
                self.raiseODMRDataRecivedEvent()

            if self.measurementType == measurementType.RabiPulse:
                self.saveRabiDataToDataFrame(data)
                self.measurementCountRabi += 1
                self.raiseRabiDataRecivedEvent()
        except Exception as ex:
            print("Error in receiving new data:", ex)
            traceback.print_exc()

    def receiveRedPitayaConnectionError(self, error):
        try:
            print("Red Pitaya connection error", error)
            self.raiseConnectionErrorEvent(error)

        except Exception:
            traceback.print_exc()

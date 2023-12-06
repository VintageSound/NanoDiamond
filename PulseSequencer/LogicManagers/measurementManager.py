import time
import traceback
import pandas as pd
import numpy as np

from Data.pulseConfiguration import pulseConfiguration
from Data.microwaveConfiguration import microwaveConfiguration

from Interfaces.redPitayaInterface import redPitayaInterface
from Interfaces.pulseBlasterInterface import pulseBlasterInterface
from Interfaces.microwaveInterface import microwaveInterface
from Data.measurementType import measurementType
from Data.repetition import repetition

# turn off microwave when rabi TODO: Test
# turn on microwave when ODMR TODO: Test
# add pulse blaster toggle TODO: Test
# TODO: add "connect to everything" method
# add load methods to data saver TODO: Test
# TODO: add complete rabi scan prosses
# TODO: add rabi scan normalization calaculation and plot the graph   
# TODO: Change "apply" method in the UI class
# TODO: add default path to save functions
# TODO: check save and load functions
# TODO: nootebook of series of measerements - Change MW, change Laser intensity, change initial pulse beginings

class measurementManager():
    maxPower = 2 ** 13  # not sure why...
    redPitayaTimeStep = redPitayaInterface.timeStep

    def __init__(self, QMainObject) -> None:
        # interfaces
        self.redPitaya = redPitayaInterface(QMainObject)
        self.pulseBlaster = pulseBlasterInterface()
        self.microwaveDevice = microwaveInterface()

        # register Events:
        self.redPitaya.registerReciveData(self.receiveDataHandler)
        self.redPitaya.registerRedPitayaConnected(self.redPitayaConnectedHandler)
        self.redPitaya.registerConnectionError(self.receiveRedPitayaConnectionError)

        # ODMR data
        self.pulseConfigODMR = pulseConfiguration()
        self.microwaveODMRConfig = microwaveConfiguration()
        self.HaveODMRData = False
        self.ODMRXAxisLabel = "Frequency [MHz]"
        self.ODMRYAxisLabel = "Photons Counted"
        self.ODMRData = None
        self.measurementCountODMR = 0
        self.initializeODMRData()

        # Rabi data
        self.pulseConfigRabi = pulseConfiguration()
        self.microwaveRabiConfig = microwaveConfiguration()
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
        self.size = 2048  # number of samples to show on the plot # max size
        self.initializeBufferODMR()

        # Events 
        self.AOMStatusChangedEvent = []
        self.redPitayaConnectedEvent = []
        self.ODMRDataRecivedEvent = []
        self.rabiPulseDataRecivedEvent = []
        self.connectionErrorEvent = []
        self.microwaveStatusChangeEvent = []

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

    # Connection Methods
    def connectToEverything(self):
        self.redPitaya.connect()
        self.pulseBlaster.connect()
        self.microwaveDevice.connect()

    def laserOpenCloseToggle(self):
        if self.redPitaya.isAOMOpen:
            self.redPitaya.closeAOM()
        else:
            self.redPitaya.congifurePulse(self.getCurrentPulseConfig())
            self.redPitaya.openAOM()

        self.raiseAOMStatusChangedEvent()

    def pulseBlasterConnectionToggle(self, ip = None, port = None):
        if self.pulseBlaster.isConnected:
            self.disconnectFromPulseBlaster()
        else:
            self.connectToPulseBlaster(ip, port)

    def connectToPulseBlaster(self, ip = None, port = None):
        if not self.pulseBlaster.isConnected:
            self.pulseBlaster.connect(ip, port)

            # TODO: check if needed
            # self.pulseBlaster.configurePulseBlaster(self.getCurrentPulseConfig(), self.measurementType)

    def disconnectFromPulseBlaster(self):
        if self.pulseBlaster.isConnected:
            self.pulseBlaster.disconnect()

    def microwaveDeviceConnectionToggle(self, config=None):
        if config is not None:
            self.microwaveConfig = config

        if self.microwaveDevice.getIsConnected():
            self.microwaveDevice.disconnect()
        else:
            self.microwaveDevice.connect()

        self.raiseMicrowaveStatusChangeEvent()

    def microwaveOnOffToggle(self):
        if not self.getIsMicrowaveConnected():
            raise Exception('Trying to send command to disconnected microwave device!')

        if self.getIsMicrowaveOn():
            self.microwaveDevice.turnOffMicrowave()
        else:
            self.microwaveDevice.turnOnMicrowave()

        self.raiseMicrowaveStatusChangeEvent()

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

        self.redPitaya.congifurePulse(self.pulseConfigODMR)
        self.pulseBlaster.configurePulseBlaster(self.pulseConfigODMR, measurementType.ODMR)

    def configurePulseSequenceForRabi(self, config=None):
        if config is not None:
            self.pulseConfigRabi = config

        self.redPitaya.congifurePulse(self.pulseConfigRabi)
        self.pulseBlaster.configurePulseBlaster(self.pulseConfigRabi, measurementType.RabiPulse)

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
        self.redPitaya.startODMR(self.pulseConfigODMR)

    def _RabiPulseMeasurement(self):
        self.redPitaya.startRabiMeasurement(self.pulseConfigRabi)

    def startNewRabiPulseMeasurement(self, 
                                    pulseConfig : pulseConfiguration = None, 
                                    micrwaveConfig : microwaveConfiguration = None):
        if pulseConfig is not None:
            self.pulseConfigRabi = pulseConfig

        if micrwaveConfig is not None:
            self.microwaveRabiConfig = micrwaveConfig

        self.measurementType = measurementType.RabiPulse
        self.isMeasurementActive = True
        self.initializeBufferRabi()
        self.configurePulseSequenceForRabi(self.pulseConfigRabi)
        self.updateMicrowaveRabiConfig(self.microwaveRabiConfig)

        self.redPitaya.closeAOM()
        self.raiseAOMStatusChangedEvent()
        
        self.microwaveDevice.turnOffMicrowave()
        self.raiseMicrowaveStatusChangeEvent()

        self._RabiPulseMeasurement()

    def startNewODMRMeasurement(self,
                                pulseConfig : pulseConfiguration = None,
                                micrwaveConfig : microwaveConfiguration = None,
                                repet=repetition.RepeatAndSum,
                                maxRepetitions=None):
        self.repetition = repet
        self.maxRepetitions = maxRepetitions

        if micrwaveConfig is not None:
            self.microwaveODMRConfig = micrwaveConfig

        if pulseConfig is not None:
            self.pulseConfigODMR = pulseConfig

        self.measurementCountODMR = 0
        self.measurementType = measurementType.ODMR
        self.isMeasurementActive = True
        self.initializeBufferODMR()
        self.configurePulseSequenceForODMR(self.pulseConfigODMR)
        self.updateMicrowaveODMRConfig(self.microwaveODMRConfig)
        
        self.microwaveDevice.turnOnMicrowave()
        self.raiseMicrowaveStatusChangeEvent()

        self.redPitaya.openAOM()
        self.raiseAOMStatusChangedEvent()

        self._ODMRMeasurement()

    def stopCurrentMeasurement(self):
        self.isMeasurementActive = False

    # Data Convertion
    def saveODMRDataToDataFrame(self, data):
        xData = np.linspace(self.microwaveODMRConfig.startFreq, self.microwaveODMRConfig.stopFreq, int(self.size / 2))
        yData = data

        # Add the recived data to the stored data if needed
        if self.repetition == repetition.RepeatAndSum:
            yData = self.ODMRData[self.ODMRYAxisLabel].tolist() + data

        self.ODMRData = pd.DataFrame({self.ODMRXAxisLabel: xData, self.ODMRYAxisLabel: yData})
        self.HaveODMRData = True

    def saveRabiDataToDataFrame(self, data):
        dataToPlot = np.array(data[0:int(self.size)], dtype=float)

        xData = np.arange(0, len(dataToPlot) * self.redPitayaTimeStep, self.redPitayaTimeStep)
        yData = dataToPlot

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

    def registerMicrowaveStatusChangeEvent(self, callback):
        self.microwaveStatusChangeEvent.append(callback)
        
    # Raise Events
    def raiseAOMStatusChangedEvent(self):
        for callback in self.AOMStatusChangedEvent:
            callback()

    def raiseMicrowaveStatusChangeEvent(self):
        for callback in self.microwaveStatusChangeEvent:
            callback()

    def raiseRedPitayaConnectedEvent(self):
        for callback in self.redPitayaConnectedEvent:
            callback()

    def raiseConnectionErrorEvent(self, error):
        for callback in self.connectionErrorEvent:
            callback(error)

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
            # TODO: Check if needed
            # self.configurePulseSequence(self.pulseConfig)
            self.raiseRedPitayaConnectedEvent()

            # Take another measurement if needed
            self.continueCurrentMeasurement()

        except Exception:
            traceback.print_exc()

    def continueCurrentMeasurement(self):
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

        # ----- delay loop -------
        time.sleep(0.5)
        # ------------------------
        self._ODMRMeasurement()

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

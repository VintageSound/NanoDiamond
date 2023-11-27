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
from Data.MeasurementType import MeasurementType

class measurementManager():
    maxPower = 2 ** 13 # not sure why...
    redPitayaTimeStep = redPitayaInterface.timeStep

    def __init__(self, QMainObject) -> None:
        # interfaces
        self.redPitaya = redPitayaInterface(QMainObject)
        self.pulseBaster = pulseBlasterInterface()
        self.microwaveDevice = microwaveInterface()
        self.dataSaver = dataSaver()

        # register Events:
        self.redPitaya.registerReciveData(self.reciveDataHandler)
        self.redPitaya.registerRedPitayaConnected(self.redPitayaConnectedHandler)
        self.redPitaya.registerConnectionError(self.reciveRedPitayaConnectionError)

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
        self.measurementType = MeasurementType.ODMR
        self.isMeasurementActive = False
        
        self.range = []
        self.repeatMeasurement = True
        self.currentIteration = int(1)
        
        # self.repeatNum = int(2000)
        self.timeStep = int(0)
        self.size = 2048  # number of samples to show on the plot # max size
        self.initalizeBufferODMR()
        
        # Events 
        self.AOMStatusChangedEvent = None
        self.redPitayaConnectedEvent = None
        self.ODMRDataRecivedEvent = None
        self.rabiPulseDataRecivedEvent = None
        self.connectionErrorEvent = None

    # Data Methods
    def initalizeBufferODMR(self):
        self.size = 2048
        self.redPitaya.initalizeBuffer(self.size * 4) # not sure why 4...    
        self.initializeODMRData()

    def initalizeBufferRabi(self):
        self.size = 1024
        self.redPitaya.initalizeBuffer(self.size * 4) # not sure why 4...        
        self.initializeRabiData()
    
    def initializeODMRData(self):
        self.HaveODMRData = False
        self.measurementCountODMR = 0
        self.ODMRData = pd.DataFrame(0, index=np.arange(1024), columns=[self.ODMRXAxisLabel, self.ODMRYAxisLabel])
       
    def initializeRabiData(self):
        self.HaveRabiData = False
        self.measurementCountRabi = 0
        self.RabiData = pd.DataFrame(0, index=np.arange(1024), columns=[self.RabiXAxisLabel, self.RabiYAxisLabel])
    
    def updateMicrowaveSweepConfig(self, config = None):
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

    def microwaveDeviceConnectionToggle(self, config = None):
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
            self.microwaveDevice.disconnect()
        else:
            self.microwaveDevice.connect()
            self.btnOn_Off.setText("RF is On")
            self.btnOn_Off.setStyleSheet("background-color:red")

    def connectToRedPitayaToggle(self, ip = None, port = None):
        if (ip is not None) and (port is not None):
            self.redPitaya.updateIpAndPort(ip, port)

        if self.getIsRedPitayaConnected():
            self.redPitaya.disconnect()
        else:
            self.redPitaya.connect()

    def configurePulseSequence(self, config = None):
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
    def _ODMRMeasuremnt(self):
        self.redPitaya.startODMR(self.pulseConfig)

    def _RabiPulseMeasurement(self):
        self.redPitaya.startRabiMeasurement(self.pulseConfig)

    def startNewRabiPulseMeasuremnt(self, config = None):
        self.measurementType = MeasurementType.SingleRabiPulse
        self.isMeasurementActive = True
        self.initalizeBufferRabi()
        self.configurePulseSequence(config)
        
        self.redPitaya.closeAOM()
        self.raiseAOMStatusChangedEvent()

        self._RabiPulseMeasurement()
    
    def startNewODMRMeasuremnt(self, config = None):
        self.measurementType = MeasurementType.ODMR
        self.isMeasurementActive = True
        self.initalizeBufferODMR()
        self.configurePulseSequence(config)
        
        self._ODMRMeasuremnt()

    def stopCurrentMeasurement(self):
        self.isMeasurementActive = False

    # Data Convertion
    def saveODMRDataToDataFrame(self, data):
        xData = np.linspace(self.microwaveConfig.startFreq, self.microwaveConfig.stopFreq, int(self.size / 2))
        yData = self.ODMRData[self.ODMRYAxisLabel].tolist() + data

        self.ODMRData = pd.DataFrame({self.ODMRXAxisLabel: xData, self.ODMRYAxisLabel: yData})
        self.HaveODMRData = True

    def saveRabiDataToDataFrame(self, data):
        dataToPlot = np.array(data[0:int(self.size)], dtype=float)

        # check if Time step is the right constant...
        self.timeStep = self.pulseConfig.CountDuration / 1000 * self.pulseConfig.CountNumber / 100 # ???
        xData = np.linspace(0, int(self.size) * self.timeStep, int(self.size))
        yData = self.RabiData[self.RabiYAxisLabel].tolist() + dataToPlot

        print("yData", yData)

        self.RabiData = pd.DataFrame({self.RabiXAxisLabel: xData, self.RabiYAxisLabel : yData})
        self.HaveRabiData = True

    
    # Register Events
    def registerToAOMStatusChangedEvent(self, eventHandler):
        if self.AOMStatusChangedEvent is not None:
            raise(Exception("AOMStatusChangedEvent allready registered!"))  
        
        self.AOMStatusChangedEvent = eventHandler

    def registerToRedPitayaConnectedEvent(self, eventHandler):
        if self.redPitayaConnectedEvent is not None:
            raise(Exception("redPitayaConnectedEvent allready registered!"))  
        
        self.redPitayaConnectedEvent = eventHandler

    def registerToODMRDataRecivedEvent(self, eventHandler):
        if self.ODMRDataRecivedEvent is not None:
            raise(Exception("ODMRDataRecivedEvent allready registered!"))  
        
        self.ODMRDataRecivedEvent = eventHandler

    def registerToRabiPulseDataRecivedEvent(self, eventHandler):
        if self.rabiPulseDataRecivedEvent is not None:
            raise(Exception("rabiPulseDataRecivedEvent allready registered!"))  
        
        self.rabiPulseDataRecivedEvent = eventHandler

    def registerConnectionErrorEvent(self, eventHandler):
        if self.connectionErrorEvent is not None:
            raise(Exception("connectionErrorEvent allready registered!"))  
        
        self.connectionErrorEvent = eventHandler
    
    # Raise Events
    def raiseAOMStatusChangedEvent(self):
        if self.AOMStatusChangedEvent is not None:
            self.AOMStatusChangedEvent()

    def raiseRedPitayaConnectedEvent(self):
        if self.redPitayaConnectedEvent is not None:
            self.redPitayaConnectedEvent()
        
    def raiseConnectionErrorEvent(self, error):
        if self.connectionErrorEvent is not None:
            self.connectionErrorEvent(error)

    def raiseODMRDataRecivedEvent(self):
        if not self.HaveODMRData:
            return

        if self.ODMRDataRecivedEvent is not None:
            self.ODMRDataRecivedEvent(self.ODMRData, self.measurementCountODMR)
        
    def raiseRabiDataRecivedEvent(self):
        if not self.HaveRabiData:
            return

        if self.rabiDataRecivedEvent is not None:
            self.rabiDataRecivedEvent(self.RabiData, self.measurementCountRabi)

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

        if not self.repeatMeasurement:
            return

        # ----- delay loop -------
        time.sleep(0.5)
        # ------------------------

        if self.measurementType == MeasurementType.ODMR:
            self._ODMRMeasuremnt()
        elif self.measurementType == MeasurementType.SingleRabiPulse:
            self._RabiMeasurement()

    def reciveDataHandler(self, data):
        try:
            if self.measurementType == MeasurementType.ODMR:
                convertedData = self.redPitaya.convertODMRData(data, self.size)
                self.saveODMRDataToDataFrame(convertedData)
                self.measurementCountODMR += 1
                self.raiseODMRDataRecivedEvent()

            if self.measurementType == MeasurementType.SingleRabiPulse:
                self.saveRabiDataToDataFrame(data)
                self.measurementCountRabi += 1
                self.raiseRabiDataRecivedEvent()
        except Exception as ex:
            print("Error in reciving new data:", ex)
            traceback.print_exc()

    def reciveRedPitayaConnectionError(self, error):
        try:
            print("Red Pitaya connection error", error)
            self.raiseConnectionErrorEvent(error)
            
        except Exception:
            traceback.print_exc()
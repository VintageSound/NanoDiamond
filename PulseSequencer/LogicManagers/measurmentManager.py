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
from Data.MeasurmentType import MeasurmentType

class measurmentManager():
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

        # MW Declarations
        self.CenterFreq = 2870.0  # Init center frequency for MW source
        self.RFPower = 0.0  # Init RF power for MW source
        self.TrigMode = 0  # Init trigger mode for MW source
        self.StartFreq = 2500.0  # Init Start frequency for MW source
        self.StopFreq = 3200.0  # Init Stop frequency for MW source

        # ODMR data
        self.microwaveConfig = microwaveConfiguration()
        self.HaveODMRData = False
        self.ODMRXAxisLabel = "Frequency [MHz]"
        self.ODMRYAxisLabel = "Photons Counted"
        self.Data = None
        self.measurmentCountODMR = 0
        self.initializeODMRData()

        # Rabi data
        self.pulseConfig = pulseConfiguration()
        self.HaveRabiData = False
        self.RabiXAxisLabel = "Time [micro seconds]"
        self.RabiYAxisLabel = "Photons Counted"
        self.RabiData = None
        self.measurmentCountRabi = 0
        self.initializeRabiData()

        # setting variables
        self.measurmentType = MeasurmentType.ODMR
        
        self.range = []
        self.repeatMeasurment = True
        self.currentIteration = int(1)
        
        self.tepeatNum = int(2000)
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

    def initalizeBuffeRabi(self):
        self.size = 1024
        self.redPitaya.initalizeBuffer(self.size * 4) # not sure why 4...        
        self.initializeRabiData()
    
    def initializeODMRData(self):
        self.HaveODMRData = False
        self.measurmentCountODMR = 0
        self.ODMRData = pd.DataFrame(0, index=np.arange(1024), columns=[self.ODMRXAxisLabel, self.ODMRYAxisLabel])
       
    def initializeRabiData(self):
        self.HaveRabiData = False
        self.measurmentCountRabi = 0
        self.RabiData = pd.DataFrame(0, index=np.arange(1024), columns=[self.RabiXAxisLabel, self.RabiYAxisLabel])
    
    def updateMicrowaveSweepConfig(self, config):
        self.microwaveConfig = config
        self.microwaveDevice.sendSweepCommand(self.microwaveConfig)

    # Connection Methods
    def laserOpenCloseToggle(self):
        if self.redPitaya.isAOMOpen:
            self.redPitaya.closeAOM()
        else:
            self.redPitaya.congifurePulse(self.pulseConfig)
            self.redPitaya.openAOM()
        
        self.raiseAOMStatusChanged()

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
            self.microwaveDevice.sendSweepCommand(self.microwaveConfig)

    def microwaveOnOffToggle(self):
        if not self.isMicrowaveConnected():
            raise Exception('Trying to send command to disconnected microwave device!')

        if self.isMicrowaveOn():
            self.microwaveDevice.disconnect()
        else:
            self.microwaveDevice.connect()
            self.btnOn_Off.setText("RF is On")
            self.btnOn_Off.setStyleSheet("background-color:red")

    def connectToRedPitayaToggle(self, ip = None, port = None):
        if (ip is not None) and (port is not None):
            self.redPitaya.updateIpAndPort(ip, port)

        if self.isRedPitayaConnected:
            self.redPitaya.disconnect()
            print("RedPitaya disconnected")
        else:
            self.redPitaya.connect()
            print("connecting to RedPitaya...")

    def configurePulseSequence(self, config = None):
        if config is not None:        
            self.pulseConfig = config

        self.redPitaya.congifurePulse(self.pulseConfig)
        self.pulseBaster.configurePulseBlaster(self.pulseConfig)

    def reconnectToRedPitaya(self):
        self.redPitaya.disconnect()
        self.redPitaya.connect()

    # Status Methods
    def isRedPitayaConnected(self):
        return self.redPitaya.isConneced

    def isLaserOpen(self):
        return self.redPitaya.isAOMOpen

    def isMicrowaveConnected(self):
        return self.microwaveDevice.getIsConnected()

    def isMicrowaveOn(self):
        return self.microwaveDevice.checkIfMicrowaveIsOn()

    # Measurment Methods
    def _ODMRMeasuremnt(self):
        self.redPitaya.startODMR(self.pulseConfig)

    def _RabiPulseMeasurment(self):
        self.redPitaya.startRabiMeasurment(self.pulseConfig)

    def startNewRabiPulseMeasuremnt(self, config = None):
        self.measurmentType = MeasurmentType.SingleRabiPulse
        self.initalizeBuffeRabi()
        self.configurePulseSequence(config)
        
        self.redPitaya.closeAOM()
        self.raiseAOMStatusChangedEvent()

        self._RabiPulseMeasurment()
    
    def startNewODMRMeasuremnt(self, config = None):
        self.measurmentType = MeasurmentType.ODMR
        self.initalizeBufferODMR()
        self.configurePulseSequence(config)
        
        self._ODMRMeasuremnt()

    # Data Convertion
    def saveODMRDataToDataFrame(self, data):
        xData = np.linspace(self.StartFreq, self.StopFreq, int(self.Size / 2))
        yData = self.ODMRData[self.ODMRYAxisLabel].tolist() + data

        self.ODMRData = pd.DataFrame({self.ODMRXAxisLabel: xData, self.ODMRYAxisLabel: yData})
        self.HaveODMRData = True

    def saveRabiDataToDataFrame(self, data):
        dataToPlot = np.array(data[0:int(self.Size)], dtype=float)

        # check if Time step is the right constant...
        xData = np.linspace(0, int(self.Size) * self.TimeStep, int(self.Size))
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
            self.ODMRDataRecivedEvent(self.ODMRData)
        
    def raiseRabiDataRecivedEvent(self):
        if not self.HaveRabiData:
            return

        if self.rabiDataRecivedEvent is not None:
            self.rabiDataRecivedEvent(self.RabiData)


        
    # Event Handlers    
    def redPitayaConnectedHandler(self):
        try:
            self.configurePulseSequence() 

            # Take another measurment if needed
            self.continueCurrentMeasurment()
        except Exception:
            traceback.print_exc()

    def continueCurrentMeasurment(self):
        if not self.repeatMeasurment:
            return

        # ----- delay loop -------
        time.sleep(0.5)
        # ------------------------

        if self.measurmentType == MeasurmentType.ODMR:
            self.ODMRMeasuremnt()
        elif self.measurmentType == MeasurmentType.SingleRabiPulse:
            self.RabiMeasurement()

    def reciveDataHandler(self, data):
        try:
            if self.measurmentType == MeasurmentType.ODMR:
                convertedData = self.redPitaya.convertODMRData(data, self.Size)
                self.saveODMRDataToDataFrame(convertedData)
                self.measurmentCountODMR += 1
                self.raiseODMRDataRecivedEvent()

            if self.measurmentType == MeasurmentType.SingleRabiPulse:
                self.saveRabiDataToDataFrame(data)
                self.measurmentCountRabi += 1
                self.raiseRabiDataRecivedEvent()

            self.reconnectToRedPitaya()
        except Exception as ex:
            print("Error in reciving new data:", ex)
            traceback.print_exc()

    def reciveRedPitayaConnectionError(self, error):
        try:
            print("Red Pitaya connection error", error)
            self.raiseConnectionErrorEvent(error)
            
        except Exception:
            traceback.print_exc()
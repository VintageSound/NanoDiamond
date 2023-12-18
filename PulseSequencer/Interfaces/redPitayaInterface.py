from PyQt5.QtNetwork import QAbstractSocket, QTcpSocket
from PyQt5.QtCore import QObject
import time
import socket
import json
import struct
import serial
import traceback
import numpy as np
import pandas as pd

from Data.pulseConfiguration import pulseConfiguration
from Data.measurementType import measurementType

class redPitayaInterface():
    _instance = None
    maxPower = 2 ** 13  #◙ not sure why...
    timeStep = 0.008 # micro second. 
    defaultRpHost = 'rp-f09ded.local'
    defaultPort = 1001

    # This is to make sure there is only one instance if the interface, so that no one will use 
    # the same connection \ socket \ series twice
    def __new__(cls, qObjectMain):
        if cls._instance is None:
            cls._instance = super(redPitayaInterface, cls).__new__(cls)
            cls._instance.initialize(qObjectMain)

        return cls._instance
        
    def initialize(self, qObjectMain):
        self.ODMRXAxisLabel = "Frequency [MHz]"
        self.ODMRYAxisLabel = "Photons Counted"
        self.RabiXAxisLabel = "Time [micro seconds]"
        self.RabiYAxisLabel = "Photons Counted"

        # TODO: check if qObjectMain is needed
        self.socket = QTcpSocket(qObjectMain)
        self.socket.connected.connect(self.connectedMessageRecived)
        self.socket.readyRead.connect(self.dataRecived)
        self.socket.error.connect(self.connectionErrorRecived)

        # set IP address and Port number
        self.ip = self.get_ip_address(redPitayaInterface.defaultRpHost)
        self.port = redPitayaInterface.defaultPort

        if self.ip:
            print(f'The IP address of {redPitayaInterface.defaultRpHost} is {self.ip}')
        else:
            print(f'Could not resolve the IP address of {redPitayaInterface.defaultRpHost}')

        # state variable
        # self.isConnected = False
        self.size = 2048
        
        self.isAOMOpen = False
        self.connectedCallBack = None
        self.reciveDataCallBack = None
        self.connectionErrorCallBack = None
        self.pulseConfig = None
        self.initializeBufferODMR()
    
    def initializeBufferODMR(self):
        self.size = 2048
        self.initializeBuffer(self.size * 4)  # God knows why is it 4 

    def initializeBufferRabi(self):
        self.size = 1024
        self.initializeBuffer(self.size * 4)  # God knows why is it 4 

    def initializeBuffer(self, bufferSize):
        self.offset = 0  
        self.bufferSize = bufferSize
        self.buffer = bytearray(self.bufferSize)
        self.data = np.frombuffer(self.buffer, np.int32)

    def getIsConnectionOpen(self):
        return self.socket.isOpen()

    def registerRedPitayaConnected(self, callback):
        self.connectedCallBack = callback

    def registerReciveData(self, callback):
        self.reciveDataCallBack = callback

    def registerConnectionError(self, callback):
        self.connectionErrorCallBack = callback

    def get_ip_address(self, rp_host):
        try:
            return socket.gethostbyname(rp_host)
        except socket.gaierror:
            return None

    def openAOM(self):
        if self.isAOMOpen:
            return

        self.socket.write(struct.pack('<Q', 16 << 58 | np.uint32(int(1))))

        self.isAOMOpen = True
        print('AOM is opened')

    def closeAOM(self):
        if not self.isAOMOpen:
            return

        self.socket.write(struct.pack('<Q', 16 << 58 | np.uint32(int(0))))

        self.isAOMOpen = False
        print('AOM is closed')

    def updateIpAndPort(self, ip, port):
        self.ip = ip
        self.port = port
                
    def connect(self, ip = None, port = None):
        if self.getIsConnectionOpen():
            return

        if ip is not None and port is not None:
            self.ip = ip 
            self.port = port

        print("trying to connect to red pitaya:", self.ip, self.port)
        self.socket.connectToHost(self.ip, self.port)

    def disconnect(self):
        if not self.getIsConnectionOpen():
            return

        print("disconnect from Red Pitaya")

        self.socket.close()
        self.offset = 0
        # self.isConnected = False

    def reconnect(self):
        self.disconnect()
        self.connect()

    def convertConfigurationToRedPitayaType(self, pulseConfig : pulseConfiguration):
        newConfig = pulseConfiguration()
        
        if pulseConfig.measurement_type == measurementType.ODMR:
            newConfig.count_duration = np.uint32(int(pulseConfig.count_duration / redPitayaInterface.timeStep))
        else:
            newConfig.count_duration = np.uint32(1)

        newConfig.count_number = np.uint32(int(np.log2(pulseConfig.count_number)))
        newConfig.threshold = np.uint32(int(pulseConfig.threshold) * redPitayaInterface.maxPower / 20) # why 20 ????
        newConfig.iterations = np.uint32(int(pulseConfig.iterations))
        newConfig.pump_start = np.uint32(int(pulseConfig.pump_start / redPitayaInterface.timeStep))
        newConfig.pump_duration = np.uint32(int(pulseConfig.pump_duration / redPitayaInterface.timeStep))
        newConfig.microwave_start = np.uint32(int(pulseConfig.microwave_start / redPitayaInterface.timeStep))
        newConfig.microwave_duration = np.uint32(int(pulseConfig.microwave_duration / redPitayaInterface.timeStep))
        newConfig.image_start = np.uint32(int(pulseConfig.image_start / redPitayaInterface.timeStep))
        newConfig.image_duration = np.uint32(int(pulseConfig.image_duration / redPitayaInterface.timeStep))
        newConfig.readout_start = np.uint32(int(pulseConfig.readout_start / redPitayaInterface.timeStep))
        newConfig.low_voltage_AOM = np.uint32(int(pulseConfig.low_voltage_AOM * redPitayaInterface.maxPower))
        newConfig.high_voltage_AOM = np.uint32(int(pulseConfig.high_voltage_AOM * redPitayaInterface.maxPower))

        return newConfig

    def congifurePulse(self, pulseConfig):
        config = self.convertConfigurationToRedPitayaType(pulseConfig)

        print(pulseConfig.high_voltage_AOM)

        self.socket.write(struct.pack('<Q', 1 << 58 | config.count_duration))
        self.socket.write(struct.pack('<Q', 2 << 58 | config.count_number))
        self.socket.write(struct.pack('<Q', 3 << 58 | config.threshold))
        self.socket.write(struct.pack('<Q', 5 << 58 | config.iterations))
        self.socket.write(struct.pack('<Q', 7 << 58 | config.pump_start))
        self.socket.write(struct.pack('<Q', 8 << 58 | config.pump_duration))
        self.socket.write(struct.pack('<Q', 9 << 58 | config.microwave_start))
        self.socket.write(struct.pack('<Q', 10 << 58 | config.microwave_duration))
        self.socket.write(struct.pack('<Q', 11 << 58 | config.image_start))
        self.socket.write(struct.pack('<Q', 12 << 58 | config.image_duration))
        self.socket.write(struct.pack('<Q', 13 << 58 | config.readout_start))
        self.socket.write(struct.pack('<Q', 14 << 58 | config.low_voltage_AOM))
        self.socket.write(struct.pack('<Q', 15 << 58 | config.high_voltage_AOM))
        self.socket.write(struct.pack('<Q', 0 << 58 | config.threshold))
        
        print("Configuration sent to red pitaya")

    def openLaserAndMicrowave(self):
        if self.isOpen:
            return

        self.socket.write(struct.pack('<Q', 16 << 58 | np.uint32(int(1))))

        self.isOpen = True
        print('Laser and MW are opened')

    def closeLaserAndMicrowave(self):
        if not self.isOpen:
            return

        self.socket.write(struct.pack('<Q', 16 << 58 | np.uint32(int(0))))

        self.isOpen = False
        print('Laser and MW are closed')

    def convertODMRData(self, data, microwaveConfig):
        # TODO: Figure out WHAT THE HELL is this code...
        # set data
        channel1 = np.array(data[0:int(self.size / 2)], dtype=float)
        channel2 = np.array(data[int(self.size / 2):self.size], dtype=float)
        convertedData = np.zeros(len(channel2)) + channel1[0]
        offset = 3.5 * channel2[0] # WHYYYYYYY

        for i in range(1, len(convertedData)):
            convertedData[i] = channel1[i] * ((channel2[0] + offset) / (channel2[i] + offset))

        x_axis = np.linspace(microwaveConfig.startFreq, microwaveConfig.stopFreq, int(self.size / 2))
        
        converted_df = pd.DataFrame({self.ODMRXAxisLabel: x_axis, self.ODMRYAxisLabel: convertedData})

        return converted_df

    def convertRabiData(self, data):
        dataToPlot = np.array(data[0:int(self.size)], dtype=float)

        # TODO: This is a mistake!! the time step is longer than we think
        x_data = np.arange(0, len(dataToPlot) * redPitayaInterface.timeStep, redPitayaInterface.timeStep)

        rabi_dataframe = pd.DataFrame({self.RabiXAxisLabel: x_data, self.RabiYAxisLabel: data})

        return rabi_dataframe

    def startODMR(self, pulseConfig : pulseConfiguration):
        config = self.convertConfigurationToRedPitayaType(pulseConfig)
        self.socket.write(struct.pack('<Q', 4 << 58 | config.count_duration))

    def startRabiMeasurement(self, pulseConfig : pulseConfiguration):
        count_duration = np.uint32(1)
        self.socket.write(struct.pack('<Q', 6 << 58 | count_duration))
        
    # ---------------- Events -----------------
    def connectedMessageRecived(self):
        try:
            print("connected to Red Pitaya!")
            # self.isConnected = True

            if self.connectedCallBack is not None:
                self.connectedCallBack()

        except Exception:
            traceback.print_exc()

    def connectionErrorRecived(self, socketError):
        if socketError == QAbstractSocket.RemoteHostClosedError:
            return

        if self.connectionErrorCallBack is not None:
            self.connectionErrorCallBack(self.socket.errorString())

    def dataRecived(self):
        try:
            size = self.socket.bytesAvailable()
            print("recived new data, bytes:", size)

            # Receive partial data
            if self.offset + size < self.bufferSize:
                self.buffer[self.offset:self.offset + size] = self.socket.read(size)
                self.offset += size

                return
            
            # Receive all data
            print("All the data was recived")
            self.buffer[self.offset:self.bufferSize] = self.socket.read(self.bufferSize - self.offset)
            
            self.offset = 0
            
            self.reconnect()
            
            if self.reciveDataCallBack is not None:
                self.reciveDataCallBack(self.data)
                    
        except Exception:
            traceback.print_exc()
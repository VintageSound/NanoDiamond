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

class QRedPitayaInterface():
    _instance = None
    maxPower = 2 ** 13  #◙ not sure why...
    timeStep = 0.008 # micro second. 
    rabiTimeStep = 0.02 # micro second. 
    defaultRpHost = 'rp-f09ded.local'
    defaultPort = 1001

    # This is to make sure there is only one instance if the interface, so that no one will use 
    # the same connection \ socket \ series twice
    def __new__(cls, qObjectMain):
        if cls._instance is None:
            cls._instance = super(QRedPitayaInterface, cls).__new__(cls)
            cls._instance.initialize(qObjectMain)

        return cls._instance
        
    def initialize(self, qObjectMain = None):
        self.ODMRXAxisLabel = "Frequency [MHz]"
        self.ODMRYAxisLabel = "Photons Counted"
        self.RabiXAxisLabel = "Time [micro seconds]"
        self.RabiYAxisLabel = "Photons Counted"

        self.socket = QTcpSocket()
        self.socket.connected.connect(self.connectedMessageRecived)
        self.socket.readyRead.connect(self.dataRecived)
        self.socket.error.connect(self.connectionErrorRecived)

        # set IP address and Port number
        self.ip = self.get_ip_address(QRedPitayaInterface.defaultRpHost)
        self.port = QRedPitayaInterface.defaultPort

        if self.ip:
            print(f'The IP address of {QRedPitayaInterface.defaultRpHost} is {self.ip}')
        else:
            print(f'Could not resolve the IP address of {QRedPitayaInterface.defaultRpHost}')

        # state variable
        # self.isConnected = False
        self.size = 2048
        
        self.isAOMOpen = False
        self.connectedCallBack = None
        self.reciveDataCallBack = None
        self.connectionErrorCallBack = None
        self.pulseConfig = None
        self.gotNewData = None
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

    def raiseNewDataRecived(self):
        if self.reciveDataCallBack is not None:
            self.reciveDataCallBack(self.data)

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

    def waitForData(self, timeout_ms = -1):
        # self.socket.readyRead.disconnect()
        
        while not self.gotNewData:
            self.socket.waitForReadyRead(timeout_ms)
            self.dataRecived()

        # self.socket.readyRead.connect(self.dataRecived())
        
        return self.data
    
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

    def waitForConnected(self, timeout_ms = 1000):
        self.socket.waitForConnected(timeout_ms)

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
            newConfig.count_duration = np.uint32(int(pulseConfig.count_duration / QRedPitayaInterface.timeStep))
        else:
            newConfig.count_duration = np.uint32(1)

        newConfig.samples_number = np.uint32(int(np.log2(pulseConfig.samples_number)))
        newConfig.threshold = np.uint32(int(pulseConfig.threshold) * QRedPitayaInterface.maxPower / 20) # why 20 ????
        newConfig.iterations = np.uint32(int(pulseConfig.iterations))
        newConfig.pump_start = np.uint32(int(pulseConfig.pump_start / QRedPitayaInterface.timeStep))
        newConfig.pump_duration = np.uint32(int(pulseConfig.pump_duration / QRedPitayaInterface.timeStep))
        newConfig.microwave_start = np.uint32(int(pulseConfig.microwave_start / QRedPitayaInterface.timeStep))
        newConfig.microwave_duration = np.uint32(int(pulseConfig.microwave_duration / QRedPitayaInterface.timeStep))
        newConfig.image_start = np.uint32(int(pulseConfig.image_start / QRedPitayaInterface.timeStep))
        newConfig.image_duration = np.uint32(int(pulseConfig.image_duration / QRedPitayaInterface.timeStep))
        newConfig.readout_start = np.uint32(int(pulseConfig.readout_start / QRedPitayaInterface.timeStep))
        newConfig.low_voltage_AOM = np.uint32(int(pulseConfig.low_voltage_AOM * QRedPitayaInterface.maxPower))
        newConfig.high_voltage_AOM = np.uint32(int(pulseConfig.high_voltage_AOM * QRedPitayaInterface.maxPower))

        return newConfig

    def congifurePulse(self, pulseConfig):
        config = self.convertConfigurationToRedPitayaType(pulseConfig)

        print(pulseConfig.high_voltage_AOM)

        self.socket.write(struct.pack('<Q', 1 << 58 | config.count_duration))
        self.socket.write(struct.pack('<Q', 2 << 58 | config.samples_number))
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
        x_data = np.arange(0, len(dataToPlot) * QRedPitayaInterface.rabiTimeStep, QRedPitayaInterface.rabiTimeStep)

        rabi_dataframe = pd.DataFrame({self.RabiXAxisLabel: x_data, self.RabiYAxisLabel: data})

        return rabi_dataframe

    def startODMR(self, pulseConfig : pulseConfiguration):
        self.gotNewData = False
        config = self.convertConfigurationToRedPitayaType(pulseConfig)
        self.socket.write(struct.pack('<Q', 4 << 58 | config.count_duration))
        print("new ODMR measurement started")

    def startRabiMeasurement(self):
        # self.socket.readyRead.connect(self.dataRecived)

        self.gotNewData = False
        count_duration = np.uint32(1)
        self.socket.write(struct.pack('<Q', 6 << 58 | count_duration))
        print("new rabi measurement started")
        
    def startRabiMeasurementSync(self, timeout = 3000):
        # self.socket.readyRead.disconnect()

        self.gotNewData = False
        count_duration = np.uint32(1)
        self.socket.write(struct.pack('<Q', 6 << 58 | count_duration))
        print("new rabi measurement started")
        
        # self.socket.waitForReadyRead(timeout)
        print("self.socket.waitForReadyRead() finished")

        while not self.proccesNewDataSync():
            # self.socket.waitForReadyRead(timeout)
            print("self.socket.waitForReadyRead() finished")

        self.reconnect()
        self.socket.waitForConnected()

        return self.data

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

    def proccesNewDataSync(self):
        size = self.socket.bytesAvailable()
        print("recived new data, bytes:", size)

        # Receive partial data
        if self.offset + size < self.bufferSize:
            self.buffer[self.offset:self.offset + size] = self.socket.read(size)
            self.offset += size

            return False
        
        # Receive all data
        print("All the data was recived")
        self.buffer[self.offset:self.bufferSize] = self.socket.read(self.bufferSize - self.offset)
        
        self.offset = 0
        return True

    def dataRecived(self):
        try:
            print("enter data recived")

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
            self.gotNewData = True

            self.reconnect()
            self.raiseNewDataRecived()        
        except Exception:
            traceback.print_exc()
import time
import socket
import json
import struct
import serial
import traceback
import numpy as np
import pandas as pd
import TimeTagger

from Data.pulseConfiguration import pulseConfiguration
from Data.measurementType import measurementType
from Data.microwaveConfiguration import microwaveConfiguration

class timeTaggerInterface():
    _instance = None
    # maxPower = 2 ** 13  #◙ not sure why...
    # timeStep = 0.008 # micro second. 
    # rabiTimeStep = 0.024 # micro second. 
    # defaultRpHost = 'rp-f09ded.local'
    # defaultPort = 1001

    # This is to make sure there is only one instance if the interface, so that no one will use 
    # the same connection \ socket \ series twice
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(timeTaggerInterface, cls).__new__(cls)
            cls._instance.initialize()

        return cls._instance
        
    def initialize(self):

        self.RabiXAxisLabel = "Time [micro seconds]"
        self.RabiYAxisLabel = "Photons Counted"
        
        # create instance of the time tagger
        self.timeTagger = TimeTagger.createTimeTagger()
        
        self.isAOMOpen = False
        self.pulseConfig = None
        self.gotNewData = None
        
    
    def initializeBufferRabi(self):
        self.size = 1024
        self.initializeBuffer(self.size * 4)  # God knows why is it 4 

    def initializeBuffer(self, bufferSize):
        self.offset = 0  
        self.bufferSize = bufferSize
        self.buffer = bytearray(self.bufferSize)
        self.data = np.frombuffer(self.buffer, np.int32)


    def openAOM(self):
        if self.isAOMOpen:
            return

        self.socket.sendall(struct.pack('<Q', 16 << 58 | np.uint32(int(1))))

        self.isAOMOpen = True
        print('AOM is opened')

    def closeAOM(self):
        if not self.isAOMOpen:
            return

        self.socket.sendall(struct.pack('<Q', 16 << 58 | np.uint32(int(0))))

        self.isAOMOpen = False
        print('AOM is closed')

    def readData(self, token):
        while token:
            try:
                data = self.socket.recv(self.bufferSize)

                if not data:
                    break

                if self.processData(data):
                    self.reconnect()
                    return self.data

            except socket.timeout:
                pass


    def readRabiData(self, token):
        self.initializeBufferRabi()
        data = self.readData(token)
        df = self.convertRabiDataToDataFrame(data)

        return df

                

    def openLaserAndMicrowave(self):
        if self.isOpen:
            return

        self.socket.sendall(struct.pack('<Q', 16 << 58 | np.uint32(int(1))))

        self.isOpen = True
        print('Laser and MW are opened')

    def closeLaserAndMicrowave(self):
        if not self.isOpen:
            return

        self.socket.sendall(struct.pack('<Q', 16 << 58 | np.uint32(int(0))))

        self.isOpen = False
        print('Laser and MW are closed')

    
    def convertRabiDataToDataFrame(self, data):
        dataToPlot = np.array(data[0:int(self.size)], dtype=float)

        # TODO: This is a mistake!! the time step is longer than we think
        x_data = np.arange(0, len(dataToPlot) * redPitayaInterface.rabiTimeStep, redPitayaInterface.rabiTimeStep)

        rabi_dataframe = pd.DataFrame({self.RabiXAxisLabel: x_data, self.RabiYAxisLabel: data})

        return rabi_dataframe


    def startRabiMeasurement(self, token):
        self.gotNewData = False
        count_duration = np.uint32(1)
        self.socket.sendall(struct.pack('<Q', 6 << 58 | count_duration))
        print("new rabi measurement started")

        return self.readRabiData(token)

    def processData(self, data):
        try:
            size = len(data)
            print("recived new data, bytes:", size)

            # Receive partial data
            if self.offset + size < self.bufferSize:
                self.buffer[self.offset:self.offset + size] = data
                self.offset += size

                return False
            
            # Receive all data
            print("All the data was recived")
            self.buffer[self.offset:self.bufferSize] = data[:(self.bufferSize - self.offset)]
            
            self.offset = 0
            self.gotNewData = True

            return True      
        except Exception:
            traceback.print_exc()


    def congifurePulse(self, pulseConfig):
        config = self.convertConfigurationToRedPitayaType(pulseConfig)

        print("AOM voltage:", pulseConfig.high_voltage_AOM)

        self.socket.sendall(struct.pack('<Q', 1 << 58 | config.count_duration))
        self.socket.sendall(struct.pack('<Q', 2 << 58 | config.samples_number))
        self.socket.sendall(struct.pack('<Q', 3 << 58 | config.threshold))
        self.socket.sendall(struct.pack('<Q', 5 << 58 | config.iterations))
        self.socket.sendall(struct.pack('<Q', 7 << 58 | config.pump_start))
        self.socket.sendall(struct.pack('<Q', 8 << 58 | config.pump_duration))
        self.socket.sendall(struct.pack('<Q', 9 << 58 | config.microwave_start))
        self.socket.sendall(struct.pack('<Q', 10 << 58 | config.microwave_duration))
        self.socket.sendall(struct.pack('<Q', 11 << 58 | config.image_start))
        self.socket.sendall(struct.pack('<Q', 12 << 58 | config.image_duration))
        self.socket.sendall(struct.pack('<Q', 13 << 58 | config.readout_start))
        self.socket.sendall(struct.pack('<Q', 14 << 58 | config.low_voltage_AOM))
        self.socket.sendall(struct.pack('<Q', 15 << 58 | config.high_voltage_AOM))
        self.socket.sendall(struct.pack('<Q', 0 << 58 | config.threshold))
        
        print("Configuration sent to red pitaya")
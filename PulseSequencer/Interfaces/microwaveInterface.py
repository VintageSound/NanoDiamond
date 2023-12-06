import json
import serial
import traceback
import numpy as np

from Data.microwaveConfiguration import microwaveConfiguration
from Data.measurementType import measurementType 

class microwaveInterface():
    _instance = None

    # This is to make sure there is only one instance if the interface, so that no one will use 
    # the same connection \ socket \ series twice
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(microwaveInterface, cls).__new__(cls)
            cls._instance.initialize()

        return cls._instance

    def initialize(self) -> None:
        self.ser = serial.Serial()
        # self.isMicrowaveOn = False

    def getIsConnected(self):
        return self.ser.is_open

    def disconnect(self):
        if not self.getIsConnected():
            return

        self.ser.write(b'E0')
        self.ser.readlines()
        self.ser.close()        

        print("WindFreak is disconnected")

    def connect(self):
        if self.getIsConnected():
            return

        self.ser = serial.Serial(
            port='COM3',
            baudrate=57600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1)

        print("WindFreak is connected")

    def checkIfMicrowaveIsOn(self):
        if not self.ser.is_open:
            raise ConnectionError('Windfreak is disconnected')
        
        self.ser.write(b'E?')

        # sometimes data returns nothing, if so - try few times
        for i in range(3):
            data = self.ser.readlines()

            if len(data) > 0:
                break

        if len(data) == 0:
            raise ConnectionError('cannot recive data from windfreak')

        if data[-1].decode('utf-8') == '1\n':
            return True
        
        return False

    def turnOnMicrowave(self):
        if not self.ser.is_open:
            raise Exception('Windfreak is disconnected')

        if not self.checkIfMicrowaveIsOn():
            self.ser.write(b'E1')

    def turnOffMicrowave(self):
        if not self.ser.is_open:
            raise Exception('Windfreak is disconnected')
        
        if self.checkIfMicrowaveIsOn():
            self.ser.write(b'E0')   

    def sendODMRSweepCommand(self, config : microwaveConfiguration):
        command = self.createSweepCommandFromConfig(config)
        self.ser.write(command)
        
        print("Windfreak ODMR configuration sent")

    def sendRabiCommand(self, config : microwaveConfiguration):
        centerFreq = ('f' + str(config.centerFreq)).encode()
        trigMode = ('w' + str(config.trigMode)).encode()
        power = ('W' + str(config.power)).encode()

        self.ser.write(power + centerFreq + trigMode)

        print("Windfreak Rabi configuration sent:", config.centerFreq, config.trigMode, config.power)

    def createSweepCommandFromConfig(self, config : microwaveConfiguration):
        power = ('W' + str(config.power)).encode()
        powerSweepStart = ('[' + str(config.powerSweepStart)).encode()
        powerSweepStop = (']' + str(config.powerSweepStop)).encode()
        startFreq = ('l' + str(config.startFreq)).encode()
        stopFreq = ('u' + str(config.stopFreq)).encode()
        stepSize = ('s' + str(config.stepSize)).encode()
        stepTime = ('t' + str(config.stepTime)).encode()
        trigMode = ('w' + str(config.trigMode)).encode()
        On = ('E1').encode()

        command = power + powerSweepStop + powerSweepStart + startFreq + stopFreq + stepTime + stepSize + trigMode + On

        return command
        

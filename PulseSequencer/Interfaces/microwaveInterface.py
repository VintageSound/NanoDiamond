import json
import serial
import traceback
import numpy as np

from Data import microwaveSweepConfiguration 

class microwaveInterface():
    def __init__(self) -> None:
        self.ser = serial.Serial()

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
            raise Exception('Windfreak is disconnected')
        
        self.ser.write(b'E?')
        data = self.ser.readlines()

        if data[0].decode('utf-8') == '1\n':
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

    def sendSweepCommand(self, config : microwaveSweepConfiguration):
        command = self.createSweepCommandFromConfig(config)

        self.ser.write(command)
        
        print("Windfreak sweep configuration sent")

    def sendSweepCommand(self, config : microwaveSweepConfiguration):
        command = self.createSweepCommandFromConfig(config)

        self.ser.write(command)
        
        print("Windfreak sweep configuration sent")

    def sendCenterFrequencyAndTriggerTypeCommand(self, config : microwaveSweepConfiguration):
        trigMode = ('w' + str(config.TrigMode)).encode()
        self.ser.write(config.enterFreq + trigMode)

        print("Windfreak configuration sent:", config.centerFreq, trigMode)

    def createSweepCommandFromConfig(self, config : microwaveSweepConfiguration):
        centerFreq = ('f' + str(config.CenterFreq)).encode()
        power = ('W' + str(config.RFPower)).encode()
        powerSweepStart = ('[' + str(config.RFPower)).encode()
        powerSweepStop = (']' + str(config.RFPower)).encode()
        startFreq = ('l' + config.txtStartFreq.text()).encode()
        stopFreq = ('u' + config.txtStopFreq.text()).encode()
        stepSize = ('s' + str(config.stepSize)).encode()
        stepTime = ('t' + str(float(config.txtCountDuration.text()) / 1000)).encode()
        trigMode = ('w' + str(config.TrigMode)).encode()
        On = ('E1').encode()

        command = power + powerSweepStop + powerSweepStart + startFreq + stopFreq + stepTime + stepSize + trigMode + On

        return command
        

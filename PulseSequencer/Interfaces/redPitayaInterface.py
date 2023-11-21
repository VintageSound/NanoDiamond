from PyQt5.QtNetwork import QAbstractSocket, QTcpSocket
from PyQt5.QtCore import QObject
import time
import socket
import json
import struct
import serial
import traceback
import numpy as np

class redPitayaInterface():
    def __init__(self, qObjectMain) -> None:
        # Create TCP socket
        # TODO: check if QTcpSocket(self) is needed
        self.socket = QTcpSocket(qObjectMain)
        self.socket.connected.connect(self.connectedMessageRecived)
        self.socket.readyRead.connect(self.dataRecived)
        self.socket.error.connect(self.connectionErrorRecived)

        # set IP address and Port number
        self.rp_host = 'rp-f09ded.local'
        self.ip = self.get_ip_address(self.rp_host)
        self.port = 1001

        if self.ip:
            print(f'The IP address of {self.rp_host} is {self.ip}')
        else:
            print(f'Could not resolve the IP address of {self.rp_host}')

        # state variable
        self.isConneced = False
        self.initalizeBuffer(1024 * 4) # Not sure why is this number...

        self.isAOMOpen = False
        self.connectedCallBack = None
        self.reciveDataCallBack = None
        self.connectionErrorCallBack = None
        self.pulseConfig = None
        self.initalizeBuffer(1024)
        
    def initalizeBuffer(self, bufferSize):
        self.offset = 0  
        self.bufferSize = bufferSize
        self.buffer = bytearray(self.bufferSize)
        self.data = np.frombuffer(self.buffer, np.int32)

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
                
    def connect(self):
        if self.isConneced:
            return

        print("trying to connect to red pitaya:", self.ip, self.port)
        self.socket.connectToHost(self.ip, self.port)

    def disconnect(self):
        if not self.isConneced:
            return

        self.socket.close()
        self.offset = 0
        self.isConneced = False
    
    def congifurePulse(self, pulseConfig):
        self.socket.write(struct.pack('<Q', 1 << 58 | pulseConfig.CountDuration))
        self.socket.write(struct.pack('<Q', 2 << 58 | pulseConfig.CountNumber))
        self.socket.write(struct.pack('<Q', 3 << 58 | pulseConfig.Threshold))
        self.socket.write(struct.pack('<Q', 5 << 58 | pulseConfig.AveragesNumber))
        self.socket.write(struct.pack('<Q', 7 << 58 | pulseConfig.StartPump))
        self.socket.write(struct.pack('<Q', 8 << 58 | pulseConfig.WidthPump))
        self.socket.write(struct.pack('<Q', 9 << 58 | pulseConfig.StartMW))
        self.socket.write(struct.pack('<Q', 10 << 58 | pulseConfig.WidthMW))
        self.socket.write(struct.pack('<Q', 11 << 58 | pulseConfig.StartImage))
        self.socket.write(struct.pack('<Q', 12 << 58 | pulseConfig.WidthImage))
        self.socket.write(struct.pack('<Q', 13 << 58 | pulseConfig.StartReadout))
        self.socket.write(struct.pack('<Q', 14 << 58 | pulseConfig.LaserLow))
        self.socket.write(struct.pack('<Q', 15 << 58 | pulseConfig.LaserHigh))
        self.socket.write(struct.pack('<Q', 0 << 58 | pulseConfig.Threshold))
        
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

    def convertODMRData(self, data, size):
        # TODO: Figure out WHAT THE HELL is this code...
        # set data
        channel1 = np.array(data[0:int(size / 2)], dtype=float)
        channel2 = np.array(data[int(size / 2):size], dtype=float)
        convertedData = np.zeros(len(channel2)) + channel1[0]
        offset = 3.5 * channel2[0] # WHYYYYYYY

        for i in range(1, len(convertedData)):
            convertedData[i] = channel1[i] * ((channel2[0] + offset) / (channel2[i] + offset))

        return convertedData

    def startODMR(self, pulseConfig):
        self.socket.write(struct.pack('<Q', 4 << 58 | pulseConfig.CountDuration))

    def startRabiMeasurment(self, pulseConfig):
        self.socket.write(struct.pack('<Q', 6 << 58 | pulseConfig.CountDuration))

    # ---------------- Events -----------------
    def connectedMessageRecived(self):
        try:
            print("connected message recived")

            self.isConnected = True

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
            print("recived new data!")
            size = self.socket.bytesAvailable()
            print("got  " + str(size))

            # Recive partial data
            if self.offset + size < self.bufferSize:
                self.buffer[self.offset:self.offset + size] = self.socket.read(size)
                self.offset += size

                return
            
            # Recive all data
            print("All the data was recived")
            self.buffer[self.offset:self.bufferSize] = self.socket.read(self.bufferSize - self.offset)
            
            self.offset = 0
            self.haveData = True # ?
            
            self.isConneced = False
            self.socket.close()
            
            if self.reciveDataCallBack is not None:
                self.reciveDataCallBack(self.data)
                    
        except Exception:
            traceback.print_exc()
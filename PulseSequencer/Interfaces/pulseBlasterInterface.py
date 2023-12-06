from PyQt5.QtNetwork import QAbstractSocket, QTcpSocket
import socket
import json
import struct
import serial
import traceback
import numpy as np

from Data.pulseConfiguration import pulseConfiguration
from Data.measurementType import measurementType

class pulseBlasterInterface():
    _instance = None
    defaultIp = "132.72.13.187"
    defaultPort = 50001

    # This is to make sure there is only one instance if the interface, so that no one will use 
    # the same connection \ socket \ series twice
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(pulseBlasterInterface, cls).__new__(cls)
            cls._instance.initialize()

        return cls._instance

    def initialize(self):
        self.server_ip = pulseBlasterInterface.defaultIp
        self.server_port = pulseBlasterInterface.defaultPort
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        self.isConnected = False

    def connect(self, ip = None, port = None):
        if self.isConnected:
            return

        if ip is not None and port is not None:
            self.server_ip = ip
            self.server_port = port

        self.client_socket.connect((self.server_ip, self.server_port))
        self.isConnected = True

    def disconnect(self):
        if not self.isConnected:
            return

        self.client_socket.close()
        self.initialize()

    def configurePulseBlaster(self, pulseConfig : pulseConfiguration, measurementType : measurementType):
        isRabi = (measurementType == measurementType.RabiPulse)

        if measurementType == measurementType.RamziPulse:
            raise NotImplementedError("ramzi not implemented!")

        data_to_send = json.dumps(
            [float(pulseConfig.StartPump), float(pulseConfig.WidthPump), float(pulseConfig.StartMW),
             float(pulseConfig.WidthMW), float(pulseConfig.StartImage), float(pulseConfig.WidthImage),
             isRabi])
        self.client_socket.send(data_to_send.encode('utf-8'))
        print("configured pulse blaster")


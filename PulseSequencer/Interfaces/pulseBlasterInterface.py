from PyQt5.QtNetwork import QAbstractSocket, QTcpSocket
import socket
import json
import struct
import serial
import traceback
import numpy as np

from Data.pulseConfiguration import pulseConfiguration

class pulseBlasterInterface():
    _instance = None

    # This is to make sure there is only one instance if the interface, so that no one will use 
    # the same connection \ socket \ series twice
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(pulseBlasterInterface, cls).__new__(cls)
            cls._instance.initialize()

        return cls._instance

    def initialize(self):
        self.server_ip = "132.72.13.187"
        self.server_port = 50001
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        self.isOpen = False

    def connect(self):
        if self.isOpen:
            return

        self.client_socket.connect((self.server_ip, self.server_port))
        self.isOpen = True

    def configurePulseBlaster(self, pulseConfig : pulseConfiguration):
        data_to_send = json.dumps(
            [float(pulseConfig.StartPump), float(pulseConfig.WidthPump), float(pulseConfig.StartMW),
             float(pulseConfig.WidthMW), float(pulseConfig.StartImage), float(pulseConfig.WidthImage),
             not self.isOpen])
        self.client_socket.send(data_to_send.encode('utf-8'))
        print("configured pulse blaster")


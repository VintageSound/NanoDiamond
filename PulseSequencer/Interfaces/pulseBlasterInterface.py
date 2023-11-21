from PyQt5.QtNetwork import QAbstractSocket, QTcpSocket
import socket
import json
import struct
import serial
import traceback
import numpy as np

from Data import pulseConfiguration 

class pulseBlasterInterface():
    def __init__(self) -> None:
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


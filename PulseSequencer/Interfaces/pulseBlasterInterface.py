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

        print("connected to pulse blaster")

    def disconnect(self):
        if not self.isConnected:
            return

        self.client_socket.close()
        self.initialize()

        print("disconnected from pulse blaster")

    def configurePulseBlaster(self, pulseConfig : pulseConfiguration):
        config_dic = {}

        if (pulseConfig.measurement_type == measurementType.RabiPulse):
            config_dic = self._createRabiDictionary(pulseConfig)
        elif (pulseConfig.measurement_type == measurementType.ODMR):
            config_dic = {"measurement_type" : measurementType.ODMR.name}
        else:
            raise NotImplementedError(pulseConfig.measurement_type.name + "not implemented")
        
        json_config = json.dumps(config_dic)
        self.client_socket.send(json_config.encode('utf-8'))
        print("configured pulse blaster")

    def _createRabiDictionary(self, pulseConfig : pulseConfiguration):        
        config_dic = {"measurement_type" : measurementType.RabiPulse.name,
                    "start_pump" : pulseConfig.pump_start,
                    "duration_pump" : pulseConfig.pump_duration,
                    "start_mw" : pulseConfig.microwave_start,
                    "start_image" : pulseConfig.image_start,
                    "duration_mw" : pulseConfig.microwave_duration}
        
        return config_dic
        


        


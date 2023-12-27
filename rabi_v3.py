import numpy as np
import sys
import struct
import serial
from datetime import datetime
import os
import traceback
import time
from PulseSequencer.Interfaces import microwaveInterfaceSMR20
import socket
import json

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtNetwork import QAbstractSocket, QTcpSocket
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtTest

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) # enable high-dpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) # use high-dpi icons

Ui_PhaseLockedLoop, QMainWindow = uic.loadUiType('odmr_v2.ui')

# declaration for pulse blaster connection
server_ip = "132.72.13.187"
server_port = 50001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))


class PhaseLockedLoop(QMainWindow, Ui_PhaseLockedLoop):
    def __init__(self):
        super(PhaseLockedLoop, self).__init__()
        self.setupUi(self)

        # setting variables
        self.idle = True  # state variable
        self.scan_idle = True
        self.open_idle = True
        self.odmr_idle = True
        self.rabi_idle = True
        self.ScanStatus = False
        self.HaveData = False
        self.Offset = 0
        self.CountDuration = 0
        self.CountNumber = 0
        self.Threshold = 0
        self.AveragesNumber = 0
        self.YData = []
        self.Channel_1 = []
        self.Channel_2 = []
        self.Range = []
        self.Step = 0
        self.Iterations = 0
        self.LaserLow = 0
        self.LaserHigh = 0
        self.CurrentIteration = int(1)
        self.StartPump, self.WidthPump = 0, 0
        self.StartMW, self.WidthMW = 0, 0
        self.StartImage, self.WidthImage = 0, 0
        self.StartReadout = 0
        self.RepeatNum = int(2000)
        self.TimeStep = int(0)
        self.Size = 1024  # number of samples to show on the plot # max size
        self.Buffer = bytearray(4 * self.Size)  # buffer and offset for the incoming samples
        self.Data = np.frombuffer(self.Buffer, np.int32)
        self.TodayDate = datetime.date(datetime.now())
        self.NormArray = []

        # MW Declarations

        self.ser = serial.Serial()
        self.CenterFreq = 2870.0  # Init center frequency for MW source
        self.RFPower = 0.0  # Init RF power for MW source
        self.TrigMode = 0  # Init trigger mode for MW source
        self.StartFreq = 2500.0  # Init Start frequency for MW source
        self.StopFreq = 3200.0  # Init Stop frequency for MW source

        # Create figure
        figure, self.axes = plt.subplots()
        figure.set_facecolor('none')
        # self.axes = figure.add_subplot(111)
        self.axes2 = self.axes.twinx()
        self.canvas = FigureCanvas(figure)
        self.plotLayout.addWidget(self.canvas)

        # Create navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.plotWidget, False)

        # Remove subplots action
        actions = self.toolbar.actions()
        self.toolbar.removeAction(actions[7])
        self.plotLayout.addWidget(self.toolbar)

        # Create TCP socket
        self.socket = QTcpSocket(self)
        self.socket.connected.connect(self.connected)
        self.socket.readyRead.connect(self.read_data)
        self.socket.error.connect(self.display_error)

        # set IP address and Port number
        def get_ip_address(rp_host):
            try:
                return socket.gethostbyname(rp_host)
            except socket.gaierror:
                return None

        rp_host = 'rp-f09ded.local'
        ip = get_ip_address(rp_host)

        if ip:
            print(f'The IP address of {rp_host} is {ip}')
        else:
            print(f'Could not resolve the IP address of {rp_host}')
        self.txtIP.setText(str(ip))
        self.txtPort.setText('1001')

        # set status bar
        self.statusBar.showMessage('Red Pitaya is disconnected')

        # settings for buttons
        self.btnConnect.clicked.connect(self.connect)
        self.btnStart.clicked.connect(self.clean_odmr)
        self.btnApply.clicked.connect(self.apply)
        self.btnMeasure.clicked.connect(self.clean_rabi)
        self.btnSave.clicked.connect(self.save)
        self.btnScanRabi.clicked.connect(self.scan)
        self.btnOpen.clicked.connect(self.open)
        self.btnConnect_2.clicked.connect(self.connect_MW_device)
        self.btnOn_Off.clicked.connect(self.mw_on_off)

        # declare Counting Duration
        self.txtCountDuration.setText('1000')
        self.txtCountDuration.textChanged.connect(self.set_config)

        # declare Counting Number
        self.txtCountNumber.setText('1024')
        self.txtCountNumber.textChanged.connect(self.set_config)

        # declare Threshold
        self.txtThreshold.setText('1.6')
        self.txtThreshold.textChanged.connect(self.set_config)

        # declare Averages Number
        self.txtAveragesNumber.setText('1')
        self.txtAveragesNumber.textChanged.connect(self.set_config)


        # ------------------------------------- Declarations for MW ---------------------------------------------------
        self.smr20 = SMR20_control.RSMR20
        self.ser = serial.Serial()
        self.txtStartFreq.setText(str(self.StartFreq))
        self.txtStopFreq.setText(str(self.StopFreq))
        self.txtCenterFreq.setText(str(self.CenterFreq))
        self.txtRFPower.setText(str(self.RFPower))
        self.comboBoxMode.setCurrentIndex(self.TrigMode)
        self.btnOn_Off.setText("RF is Off")
        # Declare operation mode
        self.comboBoxMeasureType.setCurrentIndex(0)
        # set SynthHD as default MW device
        self.comboBoxMWdevice.setCurrentIndex(0)
        # GPIB address for SMR20
        self.gpib3 = "GPIB0::3::INSTR"
        # --------------------------------------------------------------------------------------------------------------

        # declare start time and width for Rabi sequence pulses
        self.txtStartPump.setText('0')
        self.txtStartPump.textChanged.connect(self.set_config)
        self.txtWidthPump.setText('0')
        self.txtWidthPump.textChanged.connect(self.set_config)
        self.txtStartMW.setText('0')
        self.txtStartMW.textChanged.connect(self.set_config)
        self.txtWidthMW.setText('0')
        self.txtWidthMW.textChanged.connect(self.set_config)
        self.txtStartImage.setText('0')
        self.txtStartImage.textChanged.connect(self.set_config)
        self.txtWidthImage.setText('0')
        self.txtWidthImage.textChanged.connect(self.set_config)
        self.txtStartReadout.setText('0')
        self.txtStartReadout.textChanged.connect(self.set_config)

        # declare File Path
        self.txtPath.setText(r'D:/Experiments/' + str(self.TodayDate) + r'/')
        self.txtPath.textChanged.connect(self.path_changed)
        self.txtNum.setText('0')

        # populate Scan param combobox
        self.cmbScanParam.addItems(['MW width'])

        # declare Range
        self.txtRange.setText('')
        self.txtRange.editingFinished.connect(self.range_changed)

        # declare Iterations
        self.txtIterations.setText('')
        self.txtIterations.editingFinished.connect(self.iterations_changed)

        # declare Laser level
        self.txtLowLevel.setText('0.014')
        self.txtLowLevel.textChanged.connect(self.set_config)
        self.txtHighLevel.setText('0.9')
        self.txtHighLevel.textChanged.connect(self.set_config)

    def connect_MW_device(self):
        if self.comboBoxMWdevice.currentIndex() == 0:
            try:
                if self.ser.is_open:
                    self.ser.write(b'E0')
                    self.btnOn_Off.setText("RF is off")
                    self.btnOn_Off.setStyleSheet("background-color:none")
                    self.ser.readlines()
                    self.ser.close()
                    self.btnConnect_2.setText('Connect')
                    print("WindFreak is disconnected")
                else:
                    self.ser = serial.Serial(
                        port='COM3',
                        baudrate=57600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=0.1
                    )
                    print("WindFreak is connected")
                    centerFreq = ('f' + str(self.CenterFreq)).encode()
                    power = ('W' + str(self.RFPower)).encode()
                    powerSweepStart = ('[' + str(self.RFPower)).encode()
                    powerSweepStop = (']' + str(self.RFPower)).encode()
                    startFreq = ('l' + self.txtStartFreq.text()).encode()
                    stopFreq = ('u' + self.txtStopFreq.text()).encode()
                    stepSize = (self.StopFreq - self.StartFreq) / self.Size
                    stepSize = ('s' + str(stepSize)).encode()
                    stepTime = ('t' + str(float(self.txtCountDuration.text()) / 1000)).encode()
                    trigMode = ('w' + str(self.TrigMode)).encode()
                    ON = ('E1').encode()
                    self.ser.write(
                        power + powerSweepStop + powerSweepStart + startFreq + stopFreq
                        + stepTime + stepSize + trigMode + ON)
                    self.btnConnect_2.setText('Disconnect')
                    self.btnOn_Off.setText("RF is On")
                    self.btnOn_Off.setStyleSheet("background-color:red")
            except Exception:
                print('Cannot connect to windfreak')
                traceback.print_exc()
        else:
            try:
                self.smr20 = SMR20_control.RSMR20(self.gpib3)
                print(self.smr20.identify())
                self.smr20.default_values()
            except Exception:
                print('cannot connect to SMR20')
                traceback.print_exc()

    def mw_on_off(self):
        if self.comboBoxMWdevice.currentIndex() == 0:
            if self.ser.is_open:
                self.ser.write(b'E?')
                data = self.ser.readlines()
                if data[0].decode('utf-8') == '1\n':
                    self.ser.write(b'E0')
                    self.btnOn_Off.setText("RF is off")
                    self.btnOn_Off.setStyleSheet("background-color:none")
                else:
                    self.ser.write(b'E1')
                    self.btnOn_Off.setText("RF is On")
                    self.btnOn_Off.setStyleSheet("background-color:red")
            else:
                print('Windfreak is disconnected')
        else:
            if self.smr20.get_state() == '0':
                self.smr20.on()
                self.btnOn_Off.setText("RF is On")
                self.btnOn_Off.setStyleSheet("background-color:red")
            else:
                self.smr20.off()
                self.btnOn_Off.setText("RF is off")
                self.btnOn_Off.setStyleSheet("background-color:none")

    def configure_pb(self):
        # configure the pulse blaster settings
        data_to_send = json.dumps(
            [float(self.txtStartPump.text()), float(self.txtWidthPump.text()), float(self.txtStartMW.text()),
             float(self.txtWidthMW.text()), float(self.txtStartImage.text()), float(self.txtWidthImage.text()),
             self.open_idle])
        client_socket.send(data_to_send.encode('utf-8'))
        print("configured pulse blaster")

    def open(self):
        try:
            if self.open_idle:
                self.socket.write(struct.pack('<Q', 16 << 58 | np.uint32(int(1))))
                print('Laser and MW are opened')
                self.btnOpen.setText('Close')
                self.open_idle = False
                self.configure_pb()
            else:
                self.socket.write(struct.pack('<Q', 16 << 58 | np.uint32(int(0))))
                print('Laser and MW are closed')
                self.btnOpen.setText('Open')
                self.open_idle = True
                self.configure_pb()
        except Exception:
            traceback.print_exc()

    def connect(self):
        try:
            if self.idle:
                print("connecting ...")
                self.statusBar.showMessage('Red Pitaya is connecting ...')
                self.socket.connectToHost(self.txtIP.text(), int(self.txtPort.text()))
                self.btnConnect.setEnabled(False)
            else:
                self.idle = True
                self.socket.close()
                self.Offset = 0
                self.btnConnect.setText('Connect')
                self.btnConnect.setEnabled(True)
                print("Disconnected")
                self.statusBar.showMessage('Red Pitaya is disconnected')
        except Exception:
            traceback.print_exc()

    def connected(self):
        try:
            print("Connected")
            self.statusBar.showMessage('Red Pitaya is connected')
            self.idle = False
            self.btnConnect.setText('Disconnect')
            self.btnConnect.setEnabled(True)
            self.set_config()
            if self.ckbRepeat.isChecked():
                self.Channel_1 = np.zeros(int(self.Size / 2))
                self.YData = np.zeros(int(self.Size / 2))
                self.odmr_idle = True
                self.start()
            if self.ckbRepeatAdd.isChecked():
                if self.lblRepeatNum.text() == '':
                    self.lblRepeatNum.setText('0')
                self.lblRepeatNum.setText(str(int(self.lblRepeatNum.text()) + 1))
                if int(self.lblRepeatNum.text()) > self.RepeatNum - 1:
                    self.ckbRepeatAdd.setChecked(False)
                self.odmr_idle = True
                # ----- delay loop -------
                time.sleep(0.5)
                # ------------------------
                self.start()
            if self.ScanStatus:
                self.scan_idle = True
                self.scan()
                self.save()
        except Exception:
            traceback.print_exc()

    def read_data(self):
        try:
            size = self.socket.bytesAvailable()
            print("got  " + str(size))
            if self.Offset + size < 4 * self.Size:
                self.Buffer[self.Offset:self.Offset + size] = self.socket.read(size)
                self.Offset += size
            else:
                print("have all the data")
                self.Buffer[self.Offset:4 * self.Size] = self.socket.read(4 * self.Size - self.Offset)
                self.Offset = 0
                self.HaveData = True
                if self.odmr_idle:
                    self.plot_odmr()
                self.odmr_idle = False
                if self.rabi_idle:
                    self.plot_rabi()
                self.rabi_idle = False
                self.idle = True
                self.socket.close()
                self.btnStart.setEnabled(True)
                self.btnConnect.setText('Connect')
                self.connect()
        except Exception:
            traceback.print_exc()

    def display_error(self, socketError):
        try:
            if socketError == QAbstractSocket.RemoteHostClosedError:
                pass
            else:
                QMessageBox.information(self, 'PLL', 'Error: %s.' % self.socket.errorString())
            self.btnConnect.setText('Connect')
            self.btnConnect.setEnabled(True)
        except Exception:
            traceback.print_exc()

    def set_config(self):
        try:
            self.CountDuration = np.uint32(int(float(self.txtCountDuration.text()) / 0.008))
            self.CountNumber = np.uint32(int(np.log2(float(self.txtCountNumber.text()))))
            self.Threshold = np.uint32(int(float(self.txtThreshold.text()) * 2 ** 13 / 20))
            self.AveragesNumber = np.uint32(int(self.txtAveragesNumber.text()))
            self.StartPump = np.uint32(int(float(self.txtStartPump.text()) / 0.008))
            self.WidthPump = np.uint32(int(float(self.txtWidthPump.text()) / 0.008))
            self.StartMW = np.uint32(int(float(self.txtStartMW.text()) / 0.008))
            self.WidthMW = np.uint32(int(float(self.txtWidthMW.text()) / 0.008))
            self.StartImage = np.uint32(int(float(self.txtStartImage.text()) / 0.008))
            self.WidthImage = np.uint32(int(float(self.txtWidthImage.text()) / 0.008))
            self.StartReadout = np.uint32(int(float(self.txtStartReadout.text()) / 0.008))
            self.LaserLow = np.uint32(int(float(self.txtLowLevel.text()) * 2 ** 13))
            self.LaserHigh = np.uint32(int(float(self.txtHighLevel.text()) * 2 ** 13))
            if self.idle: return
            self.socket.write(struct.pack('<Q', 1 << 58 | self.CountDuration))
            self.socket.write(struct.pack('<Q', 2 << 58 | self.CountNumber))
            self.socket.write(struct.pack('<Q', 3 << 58 | self.Threshold))
            self.socket.write(struct.pack('<Q', 5 << 58 | self.AveragesNumber))
            self.socket.write(struct.pack('<Q', 7 << 58 | self.StartPump))
            self.socket.write(struct.pack('<Q', 8 << 58 | self.WidthPump))
            self.socket.write(struct.pack('<Q', 9 << 58 | self.StartMW))
            self.socket.write(struct.pack('<Q', 10 << 58 | self.WidthMW))
            self.socket.write(struct.pack('<Q', 11 << 58 | self.StartImage))
            self.socket.write(struct.pack('<Q', 12 << 58 | self.WidthImage))
            self.socket.write(struct.pack('<Q', 13 << 58 | self.StartReadout))
            self.socket.write(struct.pack('<Q', 14 << 58 | self.LaserLow))
            self.socket.write(struct.pack('<Q', 15 << 58 | self.LaserHigh))
            self.socket.write(struct.pack('<Q', 0 << 58 | self.Threshold))
            print("Configuration sent to red pitaya")
            self.configure_pb()
        except Exception:
            traceback.print_exc()

    def progress_show(self):
        try:
            for i in range(101):
                QtTest.QTest.qWait(self.TimeStep)
                self.pbarProgress.setValue(i)
        except Exception:
            traceback.print_exc()

    def start(self):
        try:
            self.socket.write(struct.pack('<Q', 4 << 58 | self.CountDuration))
            self.TimeStep = int(float(self.txtCountDuration.text()) / 1000 * int(self.txtCountNumber.text()) / 100)
            # self.smr20.software_trig(self.smr20)
            print(self.TimeStep)
            # self.progress_show()
        except Exception:
            traceback.print_exc()

    def clean_odmr(self):
        try:
            self.lblRepeatNum.setText('')
            self.Size = 2048
            self.Buffer = bytearray(4 * self.Size)
            self.Data = np.frombuffer(self.Buffer, np.int32)
            self.Channel_1 = np.zeros(int(self.Size / 2))
            self.YData = np.zeros(int(self.Size / 2))
            self.odmr_idle = True
            self.start()
        except Exception:
            traceback.print_exc()

    def clean_rabi(self):
        try:
            self.Size = 1024
            self.Channel_1 = np.zeros(int(self.Size))
            self.YData = np.zeros(int(self.Size))
            self.Buffer = bytearray(4 * self.Size)
            self.Data = np.frombuffer(self.Buffer, np.int32)
            self.rabi_idle = True
            self.measure()
        except Exception:
            traceback.print_exc()

    def apply(self):
        try:
            self.Channel_1 = np.zeros(int(self.Size / 2))
            self.YData = np.zeros(int(self.Size / 2))
            self.StartFreq = float(self.txtStartFreq.text())
            self.StopFreq = float(self.txtStopFreq.text())
            self.CenterFreq = float(self.txtCenterFreq.text())
            step_size = (self.StopFreq - self.StartFreq) / int(self.txtCountNumber.text())
            step_time = float(self.txtCountDuration.text()) / 1000
            self.RFPower = float(self.txtRFPower.text())
            self.TrigMode = self.comboBoxMode.currentIndex()
            self.plot_odmr()
            if self.comboBoxMWdevice.currentIndex() == 0:
                centerFreq = ('f' + str(self.CenterFreq)).encode()
                power = ('W' + str(self.RFPower)).encode()
                powerSweepStart = ('[' + str(self.RFPower)).encode()
                powerSweepStop = (']' + str(self.RFPower)).encode()
                startFreq = ('l' + self.txtStartFreq.text()).encode()
                stopFreq = ('u' + self.txtStopFreq.text()).encode()
                stepSize = ('s' + str(step_size)).encode()
                stepTime = ('t' + str(step_time)).encode()
                trigMode = ('w' + str(self.TrigMode)).encode()
                self.ser.write(
                    power + powerSweepStop + powerSweepStart + startFreq + stepTime + stopFreq + stepSize + trigMode)
                if self.comboBoxMeasureType.currentIndex() == 1:
                    self.comboBoxMode.setCurrentIndex(0)
                    self.TrigMode = self.comboBoxMode.currentIndex()
                    trigMode = ('w' + str(self.TrigMode)).encode()
                    print(centerFreq+trigMode)
                    self.ser.write(centerFreq + trigMode)
                print("Windfreak configuration sent")
            else:
                self.smr20.set_power(self.RFPower)
                self.smr20.set_freq_mode(1)
                self.smr20.set_sweep_parameters(self.StartFreq, self.StopFreq, step_size, step_time)
                self.smr20.set_sweep_mode(0)
                if self.comboBoxMeasureType.currentIndex() == 1:
                    self.comboBoxMode.setCurrentIndex(0)
                    self.TrigMode = self.comboBoxMode.currentIndex()
                    self.smr20.set_freq_mode(self.TrigMode)
                    # self.smr20.set_sweep_mode(self.TrigMode)
                    self.smr20.set_frequency(self.CenterFreq)
                print("SMR20 configuration sent")
        except Exception:
            traceback.print_exc()

    def measure(self):
        try:
            self.socket.write(struct.pack('<Q', 6 << 58 | self.CountDuration))
            # self.TimeStep = int(float(self.txtCountDuration.text()) / 1000 * int(self.txtCountNumber.text())
            # * int(self.txtAveragesNumber.text()) / 100)
            # self.progress_show()
        except Exception:
            traceback.print_exc()

    def path_changed(self):
        self.txtNum.setText(r'0')

    def range_changed(self):
        try:
            self.Range = []
            self.Range = self.txtRange.text().split(",")
            self.Step = float(self.Range[2])
            self.Range = np.arange(float(self.Range[0]), float(self.Range[1]) + self.Step, self.Step)
            #print(self.Range)
            #print(self.Step)
        except Exception:
            traceback.print_exc()

    def iterations_changed(self):
        try:
            self.Iterations = 0
            self.Iterations = int(self.txtIterations.text())
        except Exception:
            traceback.print_exc()

    def scan(self):
        try:
            if self.scan_idle:
                self.scan_idle = False
                self.btnScanRabi.setText('Stop')
                if self.lblCurrentValue.text() == '':
                    self.lblCurrentValue.setText(str(self.Range[0]))
                    self.CurrentIteration = 0
                    self.lblCurrentIterations.setText(str(self.CurrentIteration) + r'/' + str(self.Iterations))
                    print(self.lblCurrentIterations.text().split("/")[0])
                    self.ScanStatus = True
                else:
                    self.CurrentIteration = self.CurrentIteration + 1
                    self.lblCurrentIterations.setText(str(self.CurrentIteration) + r'/' + str(self.Iterations))
                    if int(self.CurrentIteration) > int(self.Iterations):
                        self.lblCurrentValue.setText(str(float(self.lblCurrentValue.text()) + self.Step))
                        self.CurrentIteration = 1
                        self.lblCurrentIterations.setText(str(self.CurrentIteration) + r'/' + str(self.Iterations))
                if self.cmbScanParam.currentIndex() == 0:
                    self.txtWidthMW.setText(str(self.lblCurrentValue.text()))
                self.txtParamValue.setText(str(self.lblCurrentValue.text()))
                if float(self.lblCurrentValue.text()) >= float(self.Range[-1]):
                    self.ScanStatus = False
                    self.lblCurrentValue.setText('')
                    self.scan_idle = True
                    self.btnScanRabi.setText('Scan')
                if self.ScanStatus:
                    self.clean_rabi()
            else:
                self.lblCurrentValue.setText('')
                self.lblCurrentIterations.setText('')
                self.ScanStatus = False
                self.scan_idle = True
                self.btnScanRabi.setText('Scan')
                self.save()
        except Exception:
            traceback.print_exc()

    def save(self):
        try:
            os.makedirs(self.txtPath.text(), exist_ok=True)
            data_for_save = np.loadtxt('data.csv', delimiter=',')
            settings_for_save = np.array([
                ['Measurement type: ', self.comboBoxMeasureType.currentText()],
                ['RF Power [dBm]: ', self.RFPower],
                ['Counting Duration [us]: ', self.CountDuration * 0.008],
                ['Comment: ', self.txtComment.text()],
                ['Param. value: ', self.txtParamValue.text()]
            ])
            if self.comboBoxMeasureType.currentIndex() == 1:
                print()
                settings_for_save_append = np.array([
                    ['MW frequency [MHz]: ', self.CenterFreq],
                    ['Pump pulse time [us]: ', self.StartPump],
                    ['Pump pulse duration [us]: ', self.WidthPump * 0.008],
                    ['MW pulse time [us]: ', self.StartMW * 0.008],
                    ['MW pulse duration [us]: ', self.WidthMW * 0.008],
                    ['Imaging pulse time [us]: ', self.StartImage * 0.008],
                    ['Imaging Pulse duration [us]: ', self.WidthImage * 0.008],
                    ['Readout pulse time [us]: ', self.StartReadout * 0.008],
                    ['Averages Number: ', self.AveragesNumber]
                ])
            else:
                settings_for_save_append = np.array([
                    ['Scan Start Frequency [MHz]: ', self.StartFreq],
                    ['Scan Stop Frequency [MHz]: ', self.StopFreq]
                ])
            settings_for_save = np.concatenate((settings_for_save, settings_for_save_append))
            with open(self.txtPath.text() + r'/' + self.txtNum.text() + '.csv', 'a') as file:
                np.savetxt(file, settings_for_save, delimiter=',', fmt='%s,%s')
                np.savetxt(file, data_for_save,
                           delimiter=',', fmt='%.3f,%d', header="MW frequency [MHz]" + "," + "Photon counts number")

            self.txtNum.setText(str(int(self.txtNum.text()) + 1))
        except Exception:
            traceback.print_exc()

    def plot_odmr(self):
        try:
            if not self.HaveData: return

            # reset toolbar
            self.toolbar.home()
            self.toolbar.update()

            # reset plot
            self.axes.clear()
            self.axes2.clear()
            self.axes.grid()

            # set data
            self.Channel_1 = np.array(self.Data[0:int(self.Size / 2)], dtype=float)
            self.Channel_2 = np.array(self.Data[int(self.Size / 2):self.Size], dtype=float)
            self.NormArray = np.zeros(len(self.Channel_2)) + self.Channel_1[0]
            offset = 3.5 * self.Channel_2[0]

            for i in range(1, len(self.NormArray)):
                self.NormArray[i] = self.Channel_1[i] * ((self.Channel_2[0] + offset) / (self.Channel_2[i] + offset))

            """
            # code for the adjustment of the offset value
            
            offset = np.linspace(0, 10*self.Channel_2[0], 1000)
            result = np.zeros(len(offset))
            
            for ii in range(0, len(offset)):
                for i in range(1, len(self.NormArray)):
                    self.NormArray[i] = self.Channel_1[i] * ((self.Channel_2[0] + offset[ii]) / (self.Channel_2[i] + offset[ii]))
                result[ii] = np.std(self.NormArray)

            print(offset[np.where(result == np.amin(result))[0]]/self.Channel_2[0])
            """

            x_data = np.linspace(self.StartFreq, self.StopFreq, int(self.Size / 2))
            self.YData = self.YData + self.NormArray

            xlab = "MW frequency [MHz]"
            ylab = "Photon counts number"

            np.savetxt('data.csv', np.transpose([x_data, self.YData]), fmt='%.3f,%d', delimiter=',',
                       header=xlab + "," + ylab)

            # plot

            # self.curve_1_1 = self.axes.scatter(x_data, self.Channel_1, s=1, c='red')
            #self.curve_1_2, = self.axes.plot(x_data, self.Channel_1, linewidth=0.5, c='red', label="SPCM signal")
            # self.curve_2_1 = self.axes.scatter(x_data, self.Channel_2, s=1, c='blue')
            #self.curve_2_2, = self.axes.plot(x_data, self.Channel_2, linewidth=0.5, c='blue', label="Photodiode signal")

            # self.curve_3_1 = self.axes.scatter(x_data, self.YData, s=1, c='black')
            self.curve_3_2, = self.axes.plot(x_data, self.YData, linewidth=0.5, c='black', label="Normalized signal")
            # self.curve_3_2 = self.axes.plot(offset/self.Channel_2[0], result, linewidth=0.5, c='black')
            # self.axes.set_xlim([min(x_data), max(x_data)])
            self.axes.set_xlabel(xlab)
            self.axes.set_ylabel(ylab)
            # self.axes.set_ylim([np.amin(self.Channel_1) - 200, np.amax(self.Channel_1) + 200])
            # self.axes.set_ylim([0, np.amax(self.Channel_1)])
            # self.axes2.set_ylim([0, np.amax(self.Channel_2)])
            self.axes.set_position([0.15, 0.15, 0.8, 0.8])
            self.axes.legend(loc="upper right")
            # SPCM, PD, Norm = self.axes.legend
            # SPCM.set_picker(True)
            # SPCM.set_pickradius(10)
            self.canvas.draw()
        except Exception:
            traceback.print_exc()

    def plot_rabi(self):
        try:
            if not self.HaveData: return

            # reset toolbar
            self.toolbar.home()
            self.toolbar.update()

            # reset plot
            self.axes.clear()
            self.axes2.clear()
            self.axes.grid()

            # set data
            self.Channel_1 = np.array(self.Data[0:int(self.Size)], dtype=float)

            x_data = np.linspace(self.StartFreq, self.StopFreq, int(self.Size))
            self.YData = self.YData + self.Channel_1

            xlab = "MW frequency [MHz]"
            ylab = "Photon counts number"

            np.savetxt('data.csv', np.transpose([x_data, self.YData]), fmt='%.3f,%d', delimiter=',',
                       header=xlab + "," + ylab)

            # plot
            self.curve_3_1 = self.axes.scatter(x_data, self.YData, s=1, c='black')
            self.curve_3_2 = self.axes.plot(x_data, self.YData, linewidth=0.5, c='black')
            # self.axes.set_xlim([min(x_data), max(x_data)])
            self.axes.set_xlabel(xlab)
            self.axes.set_ylabel(ylab)
            # self.axes.set_ylim([np.amin(self.Channel_1) - 200, np.amax(self.Channel_1) + 200])
            # self.axes.set_ylim([0, np.amax(self.Channel_1)])
            # self.axes2.set_ylim([0, np.amax(self.Channel_2)])
            self.axes.set_position([0.15, 0.15, 0.8, 0.8])
            self.canvas.draw()
        except Exception:
            traceback.print_exc()


app = QApplication(sys.argv)
window = PhaseLockedLoop()
window.show()
sys.exit(app.exec_())

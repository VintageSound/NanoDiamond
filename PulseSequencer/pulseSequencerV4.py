import numpy as np
import sys
from datetime import datetime
import traceback
import time
from Data.pulseConfiguration import pulseConfiguration
from Data.microwaveSweepConfiguration import microwaveSweepConfiguration
from enum import Enum

import pandas as pd

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtTest

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from Interfaces.redPitayaInterface import redPitayaInterface 
from Interfaces.pulseBlasterInterface import pulseBlasterInterface
from Interfaces.microwaveInterface import microwaveInterface
from Interfaces.dataSaver import dataSaver

class MeasurmentType(Enum):
    ODMR = 1
    Rabi = 2
    Ramzi = 3

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) # enable high-dpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) # use high-dpi icons

Ui_PhaseLockedLoop, QMainWindow = uic.loadUiType('odmr_v2.ui')

class PhaseLockedLoop(QMainWindow, Ui_PhaseLockedLoop):
    def __init__(self):
        super(PhaseLockedLoop, self).__init__()
        self.setupUi(self)

        # Interfaces intialization
        self.redPitaya = redPitayaInterface(self)
        self.pulseBaster = pulseBlasterInterface()
        self.microwaveDevice = microwaveInterface()
        self.dataSaver = dataSaver()

        # register Events:
        self.redPitaya.registerReciveData(self.reciveDataHandler)
        self.redPitaya.registerRedPitayaConnected(self.redPitayaConnectedHandler)
        self.redPitaya.registerConnectionError(self.reciveRedPitayaConnectionError)

        self.txtIP.setText(str(self.redPitaya.ip))
        self.txtPort.setText(str(self.redPitaya.port))

        # consts
        self.minTimeStep = 0.008 # micro second. redPitayaTimeStep
        self.maxPower = 2 ** 13 # not sure why...
        self.constConvertMicroSecondToMilisecond = 1000

        # data
        self.pulseConfig = pulseConfiguration()
        self.sweepConfig = microwaveSweepConfiguration()

        # setting variables
        self.measurmentType = MeasurmentType.ODMR
        self.scan_idle = True
        self.ScanStatus = False
        self.HaveODMRData = False
        self.HaveRabiData = False

        self.ODMRXAxisLabel = "Frequency [MHz]"
        self.ODMRYAxisLabel = "Photons Counted"
        self.ODMRData = None
        self.initializeODMRData()

        self.RabiXAxisLabel = "Time [micro seconds]"
        self.RabiYAxisLabel = "Photons Counted"
        self.RabiData = None
        self.initializeRabiData()

        self.Range = []
        self.CurrentIteration = int(1)
        
        self.RepeatNum = int(2000)
        self.TimeStep = int(0)
        self.Size = 1024  # number of samples to show on the plot # max size
        self.redPitaya.initalizeBuffer(self.Size * 4) # not sure why 4...
        
        self.TodayDate = datetime.date(datetime.now())
        self.NormArray = []

        # MW Declarations
        self.CenterFreq = 2870.0  # Init center frequency for MW source
        self.RFPower = 0.0  # Init RF power for MW source
        self.TrigMode = 0  # Init trigger mode for MW source
        self.StartFreq = 2500.0  # Init Start frequency for MW source
        self.StopFreq = 3200.0  # Init Stop frequency for MW source

        # Create figure
        figure, self.axes = plt.subplots()
        figure.set_facecolor('none')
        self.axes2 = self.axes.twinx()
        self.canvas = FigureCanvas(figure)
        self.plotLayout.addWidget(self.canvas)

        # Create navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.plotWidget, False)

        # Remove subplots action
        actions = self.toolbar.actions()
        self.toolbar.removeAction(actions[7])
        self.plotLayout.addWidget(self.toolbar)
   
        # set status bar
        self.statusBar.showMessage('Red Pitaya is disconnected')

        # settings for buttons
        self.btnConnect.clicked.connect(self.connectToRedPitayaToggle)
        self.btnStart.clicked.connect(self.clearAndStartODMR)
        self.btnApply.clicked.connect(self.applyChangesOfMicrowaveSettings)
        self.btnMeasure.clicked.connect(self.clearAndStartRabiMeasurment)
        self.btnSave.clicked.connect(self.save) # TODO: Change
        self.btnScanRabi.clicked.connect(self.startRabiScan)
        self.btnOpen.clicked.connect(self.laserOpenCloseToggle)
        self.btnConnect_2.clicked.connect(self.MicrowaveDeviceConnectionToggle)
        self.btnOn_Off.clicked.connect(self.microwaveOnOffToggle)

        # declare Counting Duration
        self.txtCountDuration.setText('1000')
        self.txtCountDuration.textChanged.connect(self.configurePulseSequence)

        # declare Counting Number
        self.txtCountNumber.setText('1024')
        self.txtCountNumber.textChanged.connect(self.configurePulseSequence)

        # declare Threshold
        self.txtThreshold.setText('1.6')
        self.txtThreshold.textChanged.connect(self.configurePulseSequence)

        # declare Averages Number
        self.txtAveragesNumber.setText('1')
        self.txtAveragesNumber.textChanged.connect(self.configurePulseSequence)

        # ------------------------------------- Declarations for MW ---------------------------------------------------
        self.txtStartFreq.setText(str(self.StartFreq))
        self.txtStopFreq.setText(str(self.StopFreq))
        self.txtCenterFreq.setText(str(self.CenterFreq))
        self.txtRFPower.setText(str(self.RFPower))
        self.comboBoxMode.setCurrentIndex(self.TrigMode)
        self.btnOn_Off.setText("RF is Off")
        # Declare operation mode
        self.comboBoxMeasureType.addItems([m.name for m in MeasurmentType])
        self.comboBoxMeasureType.setCurrentIndex(0)
        # set SynthHD as default MW device
        self.comboBoxMWdevice.setCurrentIndex(0)
        # --------------------------------------------------------------------------------------------------------------

        # declare start time and width for Rabi sequence pulses
        self.txtStartPump.setText('0')
        self.txtStartPump.textChanged.connect(self.configurePulseSequence)
        self.txtWidthPump.setText('4')
        self.txtWidthPump.textChanged.connect(self.configurePulseSequence)
        self.txtStartMW.setText('5')
        self.txtStartMW.textChanged.connect(self.configurePulseSequence)
        self.txtWidthMW.setText('2')
        self.txtWidthMW.textChanged.connect(self.configurePulseSequence)
        self.txtStartImage.setText('8')
        self.txtStartImage.textChanged.connect(self.configurePulseSequence)
        self.txtWidthImage.setText('4')
        self.txtWidthImage.textChanged.connect(self.configurePulseSequence)
        self.txtStartReadout.setText('0')
        self.txtStartReadout.textChanged.connect(self.configurePulseSequence)

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
        self.txtLowLevel.textChanged.connect(self.configurePulseSequence)
        self.txtHighLevel.setText('0.9')
        self.txtHighLevel.textChanged.connect(self.configurePulseSequence)

    # V
    def laserOpenCloseToggle(self):
        try:
            if self.redPitaya.isAOMOpen:
                self.redPitaya.closeAOM()
                self.btnOpen.setText('Open')
            else:
                self.redPitaya.congifurePulse(self.pulseConfig)
                self.redPitaya.openAOM()
                self.btnOpen.setText('Close')

            # Connect also to pulse blaster... TODO: change to different button
            if not self.pulseBaster.isOpen:
                self.pulseBaster.connect()
                self.pulseBaster.configurePulseBlaster(self.pulseConfig)
        except Exception:
            traceback.print_exc()

    def initializeODMRData(self):
        self.HaveODMRData = False
        self.ODMRData = pd.DataFrame(0, index=np.arange(1024), columns=[self.ODMRXAxisLabel, self.ODMRYAxisLabel])

    def initializeRabiData(self):
        self.HaveRabiData = False
        self.RabiData = pd.DataFrame(0, index=np.arange(1024), columns=[self.RabiXAxisLabel, self.RabiYAxisLabel])

    # V
    def MicrowaveDeviceConnectionToggle(self):
        try:
            if self.microwaveDevice.getIsConnected():
                self.microwaveDevice.disconnect()

                self.btnOn_Off.setText("RF is off")
                self.btnOn_Off.setStyleSheet("background-color:none")
                self.btnConnect_2.setText('Connect')
            else:
                self.microwaveDevice.connect()

                self.updateMicrowaveSweepConfig()
                self.microwaveDevice.sendSweepCommand(self.sweepConfig)
                
                self.btnOn_Off.setText("RF is On")
                self.btnOn_Off.setStyleSheet("background-color:red")
                self.btnConnect_2.setText('Disconnect')
        except Exception:
            print('Cannot connect to windfreak')
            traceback.print_exc()

    # V
    def updateMicrowaveSweepConfig(self):
        stepSize = (self.StopFreq - self.StartFreq) / int(self.txtCountNumber.text())
        stepTime = float(self.txtCountDuration.text()) / self.constConvertMicroSecondToMilisecond # convert from micro seconds to ms

        config = microwaveSweepConfiguration(
            self.CenterFreq, self.RFPower, self.RFPower, self.RFPower, 
            self.txtStartFreq.text(), self.txtStopFreq.text(), stepSize,
            stepTime, self.TrigMode)

        self.sweepConfig = config

    # V
    def microwaveOnOffToggle(self):
        try:
            if not self.microwaveDevice.getIsConnected():
                raise Exception('Trying to send command to disconnected microwave device!')

            if self.microwaveDevice.checkIfMicrowaveIsOn():
                self.microwaveDevice.disconnect()
                self.btnOn_Off.setText("RF is off")
                self.btnOn_Off.setStyleSheet("background-color:none")
            else:
                self.microwaveDevice.connect()
                self.btnOn_Off.setText("RF is On")
                self.btnOn_Off.setStyleSheet("background-color:red")

        except Exception:
            print('Error in sending command to windfreak')
            traceback.print_exc()

    # V
    def connectToRedPitayaToggle(self):
        try:
            # Connect also to pulse blaster... TODO: change to differebt button
            self.pulseBaster.connect()

            self.redPitaya.updateIpAndPort(self.txtIP.text(), int(self.txtPort.text()))

            if not self.redPitaya.isConneced:
                # Connect
                self.redPitaya.connect()
                print("connecting ...")
                self.statusBar.showMessage('Red Pitaya is connecting ...')
                self.btnConnect.setEnabled(False)

                return
            
            # Diconnect continueCurrentMeasurment
            self.redPitaya.disconnect()
            self.btnConnect.setText('Connect')
            self.btnConnect.setEnabled(True)

            print("Disconnected")
            self.statusBar.showMessage('Red Pitaya is disconnected')

        except Exception:
            traceback.print_exc()

    # V
    # TODO: Divide into more methods..
    def redPitayaConnectedHandler(self):
        try:
            print("Connected")
            self.statusBar.showMessage('Red Pitaya is connected')
            self.btnConnect.setText('Disconnect')
            self.btnConnect.setEnabled(True)

            self.configurePulseSequence()  # why?

            if self.ckbRepeat.isChecked():
                self.Channel_1 = np.zeros(int(self.Size / 2))
                self.YData = np.zeros(int(self.Size / 2))
                self.continueCurrentMeasurment()

            if self.ckbRepeatAdd.isChecked():
                if self.lblRepeatNum.text() == '':
                    self.lblRepeatNum.setText('0')

                self.lblRepeatNum.setText(str(int(self.lblRepeatNum.text()) + 1))

                if int(self.lblRepeatNum.text()) >= self.RepeatNum:
                    self.ckbRepeatAdd.setChecked(False)

                # ----- delay loop -------
                time.sleep(0.5)
                # ------------------------
                self.continueCurrentMeasurment()

            if self.ScanStatus:
                self.scan_idle = True
                self.scan()
                self.save()

        except Exception:
            traceback.print_exc()

    def continueCurrentMeasurment(self):
        if self.measurmentType == MeasurmentType.ODMR:
            self.startODMR()
        elif self.measurmentType == MeasurmentType.Rabi:
            self.startRabiMeasurement()

    # V
    def reciveDataHandler(self, data):
        try:
            if self.measurmentType == MeasurmentType.ODMR:
                convretedData = self.redPitaya.convertODMRData(data, self.Size)
                self.convertODMRDataToDataFrame(convretedData)
                self.plotODMRData()

            if self.measurmentType == MeasurmentType.Rabi:
                self.convertRabiDataToDataFrame(data)
                self.plotRabiData()

            self.btnStart.setEnabled(True)
            self.btnConnect.setText('Connect')

            self.redPitaya.disconnect()
            self.redPitaya.connect()

        except Exception:
            traceback.print_exc()

    # V
    def convertODMRDataToDataFrame(self, data):
        xData = np.linspace(self.StartFreq, self.StopFreq, int(self.Size / 2))
        yData = self.ODMRData[self.ODMRYAxisLabel].tolist() + data

        self.ODMRData = pd.DataFrame({self.ODMRXAxisLabel: xData, self.ODMRYAxisLabel: yData})
        self.HaveODMRData = True

    # V
    def convertRabiDataToDataFrame(self, data):
        # TODO: Check if Works...
        print("data", data)

        dataToPlot = np.array(data[0:int(self.Size)], dtype=float)

        # check if Time step is the right constant...
        xData = np.linspace(0, int(self.Size) * self.TimeStep, int(self.Size))
        yData = self.RabiData[self.RabiYAxisLabel].tolist() + dataToPlot

        print("yData", yData)

        self.RabiData = pd.DataFrame({self.RabiXAxisLabel: xData, self.RabiYAxisLabel : yData})
        self.HaveRabiData = True

    # V
    def reciveRedPitayaConnectionError(self, error):
        try:
            QMessageBox.information(self, 'PLL', 'Error: %s.' % error)
            self.btnConnect.setText('Connect')
            self.btnConnect.setEnabled(True)
        except Exception:
            traceback.print_exc()
    
    # V
    def configurePulseSequence(self):
        try:
            # TODO: regard ramsi and multipule rabi when needed
            if self.measurmentType == MeasurmentType.Rabi:
                self.pulseConfig.CountDuration = np.uint32(1)
            else:
                self.pulseConfig.CountDuration = np.uint32(int(float(self.txtCountDuration.text()) / self.minTimeStep))

            self.pulseConfig.CountNumber = np.uint32(int(np.log2(float(self.txtCountNumber.text()))))
            self.pulseConfig.Threshold = np.uint32(int(float(self.txtThreshold.text()) * self.maxPower / 20)) # why 20 ????
            self.pulseConfig.AveragesNumber = np.uint32(int(self.txtAveragesNumber.text()))
            self.pulseConfig.StartPump = np.uint32(int(float(self.txtStartPump.text()) / self.minTimeStep))
            self.pulseConfig.WidthPump = np.uint32(int(float(self.txtWidthPump.text()) / self.minTimeStep))
            self.pulseConfig.StartMW = np.uint32(int(float(self.txtStartMW.text()) / self.minTimeStep))
            self.pulseConfig.WidthMW = np.uint32(int(float(self.txtWidthMW.text()) / self.minTimeStep))
            self.pulseConfig.StartImage = np.uint32(int(float(self.txtStartImage.text()) / self.minTimeStep))
            self.pulseConfig.WidthImage = np.uint32(int(float(self.txtWidthImage.text()) / self.minTimeStep))
            self.pulseConfig.StartReadout = np.uint32(int(float(self.txtStartReadout.text()) / self.minTimeStep))
            self.pulseConfig.LaserLow = np.uint32(int(float(self.txtLowLevel.text()) * self.maxPower))
            self.pulseConfig.LaserHigh = np.uint32(int(float(self.txtHighLevel.text()) * self.maxPower))

            self.redPitaya.congifurePulse(self.pulseConfig)
            self.pulseBaster.configurePulseBlaster(self.pulseConfig)
        except Exception:
            traceback.print_exc()

    # V
    def startODMR(self):
        try:
            self.measurmentType = MeasurmentType.ODMR
            self.configurePulseSequence()
            self.redPitaya.startODMR(self.pulseConfig)

            # Not sure what is this...
            self.TimeStep = int(float(self.txtCountDuration.text()) / 1000 * int(self.txtCountNumber.text()) / 100)
        except Exception:
            traceback.print_exc()

    # V
    def clearAndStartODMR(self):
        try:
            self.Size = 2048
            self.redPitaya.initalizeBuffer(self.Size * 4) # not sure why 4...
            
            self.lblRepeatNum.setText('')

            self.initializeODMRData()
            
            self.HaveODMRData = False

            self.startODMR()
        except Exception:
            traceback.print_exc()

    # V
    def clearAndStartRabiMeasurment(self):
        try:
            self.Size = 1024
            self.redPitaya.initalizeBuffer(self.Size * 4) # not sure why 4...

            self.measurmentType = MeasurmentType.Rabi
            self.redPitaya.closeAOM()
            self.btnOpen.setText('Open')
            self.configurePulseSequence()

            self.initializeRabiData()

            self.HaveRabiData = False

            self.startRabiMeasurement()

        except Exception:
            traceback.print_exc()

    # V
    def applyChangesOfMicrowaveSettings(self):
        try:
            self.StartFreq = float(self.txtStartFreq.text())
            self.StopFreq = float(self.txtStopFreq.text())
            self.CenterFreq = float(self.txtCenterFreq.text())
            self.RFPower = float(self.txtRFPower.text())
            self.TrigMode = self.comboBoxMode.currentIndex()
            
            # TODO: Check if works and if neccerey
            self.plotODMRData()

            self.updateMicrowaveSweepConfig()
            self.microwaveDevice.sendSweepCommand(self.sweepConfig)

            # TODO: CHANGE to map (do not trust UI indexes!)
            if self.comboBoxMeasureType.currentIndex() == 1:
                self.comboBoxMode.setCurrentIndex(0)

                # TODO: CHANGE to map (do not trust UI indexes!)
                self.TrigMode = self.comboBoxMode.currentIndex()
                           
        except Exception:
            traceback.print_exc()

    # V
    def startRabiMeasurement(self):
        try:
            self.measurmentType = MeasurmentType.Rabi
            self.redPitaya.startRabiMeasurment(self.pulseConfig)
        except Exception:
            traceback.print_exc()

    # V
    def path_changed(self):
        self.txtNum.setText(r'0')

    # V
    def range_changed(self):
        try:
            self.Range = []
            self.Range = self.txtRange.text().split(",")
            self.Step = float(self.Range[2])
            self.Range = np.arange(float(self.Range[0]), float(self.Range[1]) + self.Step, self.Step)
        except Exception:
            traceback.print_exc()

    # V
    def iterations_changed(self):
        try:
            self.Iterations = 0
            self.Iterations = int(self.txtIterations.text())
        except Exception:
            traceback.print_exc()

    # V
    #TODO: Rewrite to make sense...
    def startRabiScan(self):
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
                    self.clearAndStartRabiMeasurment()
            else:
                self.lblCurrentValue.setText('')
                self.lblCurrentIterations.setText('')
                self.ScanStatus = False
                self.scan_idle = True
                self.btnScanRabi.setText('Scan')
                self.save()
        except Exception:
            traceback.print_exc()

    # X
    def saveODMR(self):
        metadata = {'Measurement type:': MeasurmentType.ODMR.name,
                'RF Power [dBm]:': self.pulseConfig.RFPower,
                'Measurment Duration [us]:': self.pulseConfig.CountDuration * self.minTimeStep,
                'Comment:': self.txtComment.text(),
                'Param. value:': self.txtParamValue.text(),
                'Scan Start Frequency [MHz]:': self.sweepConfig.startFreq,
                'Scan Stop Frequency [MHz]:': self.sweepConfig.stopFreq}

        filePath = self.createFilePath()
        self.dataSaver.save(filePath, metadata, self.ODMRData)

    def saveRabi(self):
        metadata = {'Measurement type': MeasurmentType.Rabi.name,
                    'RF Power [dBm]': self.pulseConfig.RFPower,
                    'Measurement Duration [us]': self.pulseConfig.CountDuration * self.minTimeStep,
                    'Comment': self.txtComment.text(),
                    'Param. value': self.txtParamValue.text(),
                    'MW frequency [MHz]': self.pulseConfig.CenterFreq,
                    'Pump pulse time [us]': self.pulseConfig.StartPump,
                    'Pump pulse duration [us]': self.pulseConfig.WidthPump * self.minTimeStep,
                    'MW pulse time [us]': self.pulseConfig.StartMW * self.minTimeStep,
                    'MW pulse duration [us]': self.pulseConfig.WidthMW * self.minTimeStep,
                    'Imaging pulse time [us]': self.pulseConfig.StartImage * self.minTimeStep,
                    'Imaging Pulse duration [us]': self.pulseConfig.WidthImage * self.minTimeStep,
                    'Readout pulse time [us]': self.pulseConfig.StartReadout * self.minTimeStep,
                    'Averages Number': self.pulseConfig.AveragesNumber}

        filePath = self.createFilePath()
        dataSaver.save(filePath, metadata, self.RabiData)

    def createFilePath(self):
        filePath = self.txtPath.text() + r'/' + self.measurmentType.name + '_' + self.txtNum.text() + '.csv'
        return filePath

    def save(self):

        if self.measurmentType == MeasurmentType.ODMR:
            self.saveODMR()
        elif self.measurmentType == MeasurmentType.Rabi:
            self.saveRabi()

        # try:
        #     os.makedirs(self.txtPath.text(), exist_ok=True)
        #     data_for_save = np.loadtxt('data.csv', delimiter=',')
        #     settings_for_save = np.array([
        #         ['Measurement type: ', self.comboBoxMeasureType.currentText()],
        #         ['RF Power [dBm]: ', self.RFPower],
        #         ['Counting Duration [us]: ', self.CountDuration * 0.008],
        #         ['Comment: ', self.txtComment.text()],
        #         ['Param. value: ', self.txtParamValue.text()]
        #     ])
        #     if self.comboBoxMeasureType.currentIndex() == 1:
        #         print()
        #         settings_for_save_append = np.array([
        #             ['MW frequency [MHz]: ', self.CenterFreq],
        #             ['Pump pulse time [us]: ', self.StartPump],
        #             ['Pump pulse duration [us]: ', self.WidthPump * 0.008],
        #             ['MW pulse time [us]: ', self.StartMW * 0.008],
        #             ['MW pulse duration [us]: ', self.WidthMW * 0.008],
        #             ['Imaging pulse time [us]: ', self.StartImage * 0.008],
        #             ['Imaging Pulse duration [us]: ', self.WidthImage * 0.008],
        #             ['Readout pulse time [us]: ', self.StartReadout * 0.008],
        #             ['Averages Number: ', self.AveragesNumber]
        #         ])
        #     else:
        #         settings_for_save_append = np.array([
        #             ['Scan Start Frequency [MHz]: ', self.StartFreq],
        #             ['Scan Stop Frequency [MHz]: ', self.StopFreq]
        #         ])
        #     settings_for_save = np.concatenate((settings_for_save, settings_for_save_append))
        #     with open(self.txtPath.text() + r'/' + self.txtNum.text() + '.csv', 'a') as file:
        #         np.savetxt(file, settings_for_save, delimiter=',', fmt='%s,%s')
        #         np.savetxt(file, data_for_save,
        #                    delimiter=',', fmt='%.3f,%d', header="MW frequency [MHz]" + "," + "Photon counts number")

        #     self.txtNum.setText(str(int(self.txtNum.text()) + 1))
        # except Exception:
        #     traceback.print_exc()

    # V
    def plotODMRData(self):
        try:
            if not self.HaveODMRData : return

            # reset toolbar
            self.toolbar.home()
            self.toolbar.update()

            # reset plot
            self.axes.clear()
            self.axes2.clear()
            self.axes.grid()

            # TODO: Check if work
            # plot
            self.curve_3_2, = self.axes.plot(self.ODMRData[self.ODMRXAxisLabel], self.ODMRData[self.ODMRYAxisLabel], linewidth=0.5, c='black', label="Normalized signal")
            self.axes.set_xlabel(self.ODMRXAxisLabel)
            self.axes.set_ylabel(self.ODMRYAxisLabel)
            self.axes.set_position([0.15, 0.15, 0.8, 0.8])
            self.axes.legend(loc="upper right")
            
            self.canvas.draw()
        except Exception:
            traceback.print_exc()

    # V
    def plotRabiData(self):
        try:
            if not self.HaveRabiData: return

            # reset toolbar
            self.toolbar.home()
            self.toolbar.update()

            # reset plot
            self.axes.clear()
            self.axes2.clear()
            self.axes.grid()

            # plot
            print(self.RabiData)

            # TODO: Check if works
            self.curve_3_1 = self.axes.scatter(self.RabiData[self.RabiXAxisLabel], self.RabiData[self.RabiYAxisLabel], s=1, c='black')
            self.curve_3_2 = self.axes.plot(self.RabiData[self.RabiXAxisLabel], self.RabiData[self.RabiYAxisLabel], linewidth=0.5, c='black')
            
            self.axes.set_xlabel(self.RabiXAxisLabel)
            self.axes.set_ylabel(self.RabiYAxisLabel)
            
            self.axes.set_position([0.15, 0.15, 0.8, 0.8])
            self.canvas.draw()
        except Exception:
            traceback.print_exc()

app = QApplication(sys.argv)
window = PhaseLockedLoop()
window.show()
sys.exit(app.exec_())
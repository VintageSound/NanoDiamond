import numpy as np
import sys
import traceback
import time

from Data.pulseConfiguration import pulseConfiguration
from Data.microwaveConfiguration import microwaveConfiguration
from Data.measurementType import measurementType
from Data.repetition import repetition

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtTest

import matplotlib

from Interfaces.dataSaver import dataSaver

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from LogicManagers.measurementManager import measurementManager

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) # enable high-dpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) # use high-dpi icons

try:
    Ui_PhaseLockedLoop, QMainWindow = uic.loadUiType('PulseSequencerV4.ui')
except:
    Ui_PhaseLockedLoop, QMainWindow = uic.loadUiType('PulseSequencer\\PulseSequencerV4.ui')

constConvertMicroSecondToMilisecond = 1000

class PhaseLockedLoop(QMainWindow, Ui_PhaseLockedLoop):    
    def __init__(self):
        super(PhaseLockedLoop, self).__init__()
        self.setupUi(self)
        self.measurementManager = measurementManager(self)
        self.dataSaver = dataSaver(self.measurementManager)

        self.txtIPRedPitaya.setText(str(self.measurementManager.redPitaya.ip))
        self.txtPortRedPitaya.setText(str(self.measurementManager.redPitaya.port))

        self.txtIPPulseBlaster.setText(str(self.measurementManager.pulseBlaster.server_ip))
        self.txtPortPulseBlaster.setText(str(self.measurementManager.pulseBlaster.server_port))
        self.repetitionComboBox.addItems([m.name for m in repetition])

        # Register Events
        self.measurementManager.registerToAOMStatusChangedEvent(self.laserStatusChangedEventHandler)
        self.measurementManager.registerToRedPitayaConnectedEvent(self.redPitayaConnectedHandler)
        
        self.measurementManager.registerToRabiPulseDataRecivedEvent(self.reciveRabiDataHandler)
        self.measurementManager.registerToODMRDataRecivedEvent(self.reciveODMRDataHandler)
        self.measurementManager.registerConnectionErrorEvent(self.connectionErrorEventHandler)
        self.measurementManager.registerMicrowaveStatusChangeEvent(self.microwaveStatusChanged)

        # settings for buttons
        # general
        self.btnConnectPulseBlaster.clicked.connect(self.connectToPulseBlasterToggle)
        self.btnConnectRedPitaya.clicked.connect(self.connectToRedPitayaToggle)

        # ODMR
        self.btnStartODMR.clicked.connect(self.clearAndStartODMR)
        self.btnStopODMR.clicked.connect(self.stopCurrentMeasurement)
        self.btnOpenCloseAOM.clicked.connect(self.laserOpenCloseToggle)
        self.connectMicrowaveODMRButton.clicked.connect(self.microwaveDeviceConnectionToggle)
        self.onOffODMRConnectButton.clicked.connect(self.microwaveOnOffToggle)
        self.btnSaveODMR.clicked.connect(self.saveODMR)

        # rabi
        self.btnMeasureRabiPulse.clicked.connect(self.clearAndStartRabiMeasurement)
        self.connectMicrowaveRabiButton.clicked.connect(self.microwaveDeviceConnectionToggle)
        self.onOffRabiConnectButton.clicked.connect(self.microwaveOnOffToggle)
        self.btnSaveRabi.clicked.connect(self.saveRabi)

        # initialize axes
        self.initializeODMRAxes()
        self.initializeRabiAxes()

        # TODO: Add full rabi sequence
        # self.btnScanRabi.clicked.connect(self.startRabiScan)

        # declare Counting Duration
        self.txtCountDuration.setText('1000')

        # declare Counting Number
        self.txtCountNumber.setText('1024')
        
        # declare Threshold
        self.txtThreshold.setText('1.6')

        # declare Averages Number
        self.txtAveragesNumber.setText('1')
        
        # ------------------------------------- Declarations for MW ---------------------------------------------------
        self.txtStartFreq.setText("2500")
        self.txtStopFreq.setText("3200")
        self.txtCenterFreq.setText("2870")
        self.txtRFPower.setText("0")
        self.txtRFPowerRabi.setText("0")
        self.onOffRabiConnectButton.setText("RF is Off")
        self.onOffODMRConnectButton.setText("RF is Off")
        # --------------------------------------------------------------------------------------------------------------

        # declare start time and width for Rabi sequence pulses
        self.txtStartPump.setText('0')
        self.txtWidthPump.setText('4')
        self.txtStartMW.setText('5')
        self.txtWidthMW.setText('2')
        self.txtStartImage.setText('8')
        self.txtWidthImage.setText('4')
        self.txtStartReadout.setText('0')
        
        # declare File Path
        # self.txtPath.setText(self.measurementManager.dataSaver.getFolderToSave())
        # self.txtPath.textChanged.connect(self.path_changed)
        # self.txtNum.setText('0')

        # declare Laser level
        self.txtLowLevel.setText('0.014')
        self.txtHighLevel.setText('0.9')

    # Initialization Methods
    def initializeODMRAxes(self):
        # Create figure
        figure, self.axesODMR = plt.subplots()
        figure.set_facecolor('none')

        self.odmrCanvas = FigureCanvas(figure)
        self.ODMRPlotLayout.addWidget(self.odmrCanvas)

        # Create navigation toolbar
        self.ODMRToolbar = NavigationToolbar(self.odmrCanvas, self.ODMRPlotWidget, False)

        # Remove subplots action
        actions = self.ODMRToolbar.actions()
        self.ODMRToolbar.removeAction(actions[7])
        self.ODMRPlotLayout.addWidget(self.ODMRToolbar)

    def initializeRabiAxes(self):
        # Create figure
        figure, self.axesRabi1 = plt.subplots()
        figure.set_facecolor('none')

        self.axesRabi2 = self.axesRabi1.twinx()

        self.rabiCanvas = FigureCanvas(figure)
        self.rabiPulsePlotLayout.addWidget(self.rabiCanvas)

        # Create navigation toolbar
        self.rabiToolbar = NavigationToolbar(self.rabiCanvas, self.rabiPulsePlotWidget, False)

        # Remove subplots action
        actions = self.rabiToolbar.actions()
        self.rabiToolbar.removeAction(actions[7])
        self.rabiPulsePlotLayout.addWidget(self.rabiToolbar)

    # Getters
    def getCurrentMeasurementTab(self):
        if self.measurmentTabs.currentIndex() == measurementType.ODMR.value:
            return measurementType.ODMR

        if self.measurmentTabs.currentIndex() == measurementType.RabiPulse.value:
            return measurementType.RabiPulse

        raise NotImplementedError("Ramsey not implemented")

    # Action Methods
    def laserOpenCloseToggle(self):
        try:
            self.measurementManager.laserOpenCloseToggle()
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def microwaveDeviceConnectionToggle(self):
        try:
            self.measurementManager.microwaveDeviceConnectionToggle()
        except Exception as ex:
            print('Cannot connect to windfreak', ex)
            traceback.print_exc()

    def microwaveOnOffToggle(self):
        try:
            self.measurementManager.microwaveOnOffToggle()
        except Exception as ex:
            print('Error in sending command to windfreak', ex)
            traceback.print_exc()

    def connectToRedPitayaToggle(self):
        try:
            self.measurementManager.connectToRedPitayaToggle(self.txtIPRedPitaya.text(), int(self.txtPortRedPitaya.text()))

            if self.measurementManager.getIsRedPitayaConnected():
                # Wait for connection event to enable the button  
                self.btnConnectRedPitaya.setEnabled(False)
            else:
                self.btnConnectRedPitaya.setText('Connect')
                self.btnConnectRedPitaya.setEnabled(True)
        except Exception:
            traceback.print_exc()

    def connectToPulseBlasterToggle(self):
        try:
            ip = self.txtIPPulseBlaster.text()
            port = int(self.txtPortPulseBlaster.text())
        
            self.measurementManager.pulseBlasterConnectionToggle(ip, port)

            if self.measurementManager.getIsPulseBlasterConnected():
                self.btnConnectPulseBlaster.setText('Disconnect')
            else:
                self.btnConnectPulseBlaster.setText('Connect')
        except Exception:
            traceback.print_exc()

    def clearAndStartODMR(self):
        try:
            self.lblCurrentRepetetion.setText('0')
            microwave_config = self.createRabiMicrowaveConfig()
            pulse_config = self.createPulseConfiguration()
            repeat = repetition[self.repetitionComboBox.currentText()]

            max_repetitions = self.txtRepetitionMax.text()

            if max_repetitions == "":
                max_repetitions = None
            else:
                max_repetitions = int(max_repetitions)

            self.measurementManager.startNewODMRMeasurement(pulse_config, microwave_config, repeat, max_repetitions)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def stopCurrentMeasurement(self):
        try:
            self.measurementManager.stopCurrentMeasurement()
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def clearAndStartRabiMeasurement(self):
        try:
            microwave_config = self.createRabiMicrowaveConfig()
            pulse_config = self.createPulseConfiguration()
            self.measurementManager.startNewRabiPulseMeasurement(pulse_config, microwave_config)
        except Exception:
            traceback.print_exc()

    def indicateMicrowaveIsConnected(self):
        self.connectMicrowaveODMRButton.setText('Disconnect')
        self.connectMicrowaveRabiButton.setText('Disconnect')

    def indicateMicrowaveIsDisconnected(self):
        self.connectMicrowaveODMRButton.setText('Connect')
        self.connectMicrowaveRabiButton.setText('Connect')
        self.indicateMicrowaveIsOff()

    def indicateMicrowaveIsOn(self):
        self.onOffODMRConnectButton.setText("RF is On")
        self.onOffRabiConnectButton.setText("RF is On")
        
        self.onOffODMRConnectButton.setStyleSheet("background-color:red")
        self.onOffRabiConnectButton.setStyleSheet("background-color:red")

    def indicateMicrowaveIsOff(self):
        self.onOffODMRConnectButton.setText("RF is off")
        self.onOffRabiConnectButton.setText("RF is off")
        
        self.onOffODMRConnectButton.setStyleSheet("background-color:none")
        self.onOffRabiConnectButton.setStyleSheet("background-color:none")

    # TODO: Add Save
    def saveODMR(self):
        try:
            self.dataSaver.setODMRFolderToSave(self.ODMRPathTextBox.text())
            self.dataSaver.ODMRIndex = int(self.ODMRFileNumber.text())

            comment = self.ODMRComment.text()

            self.dataSaver.saveODMR(comment)      
            self.ODMRFileNumber.setText(str(self.dataSaver.ODMRIndex))
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    # TODO: ADd
    def saveRabi(self):
        pass 
    # def save(self):
    #     try:
    #         if self.measurmentTabs.currentIndex() == measurementType.ODMR.value:
    #             self.saveODMR()
    #         elif self.measurmentTabs.currentIndex() == measurementType.RabiPulse.value:
    #             self.saveRabi()
    #     except Exception as ex:
    #         print(ex)
    #         traceback.print_exc()

    # Config Methods
    def createPulseConfiguration(self):
        try:
            timeStep = measurementManager.redPitayaTimeStep
            pulseConfig = pulseConfiguration()

            type = self.getCurrentMeasurementTab()

            if type == measurementType.ODMR:
                pulseConfig.CountDuration = np.uint32(int(float(self.txtCountDuration.text()) / timeStep))
            else:
                pulseConfig.CountDuration = np.uint32(1)

            pulseConfig.CountNumber = np.uint32(int(np.log2(float(self.txtCountNumber.text()))))
            pulseConfig.Threshold = np.uint32(int(float(self.txtThreshold.text()) * measurementManager.maxPower / 20)) # why 20 ????
            pulseConfig.AveragesNumber = np.uint32(int(self.txtAveragesNumber.text()))
            pulseConfig.StartPump = np.uint32(int(float(self.txtStartPump.text()) / timeStep))
            pulseConfig.WidthPump = np.uint32(int(float(self.txtWidthPump.text()) / timeStep))
            pulseConfig.StartMW = np.uint32(int(float(self.txtStartMW.text()) / timeStep))
            pulseConfig.WidthMW = np.uint32(int(float(self.txtWidthMW.text()) / timeStep))
            pulseConfig.StartImage = np.uint32(int(float(self.txtStartImage.text()) / timeStep))
            pulseConfig.WidthImage = np.uint32(int(float(self.txtWidthImage.text()) / timeStep))
            pulseConfig.StartReadout = np.uint32(int(float(self.txtStartReadout.text()) / timeStep))
            pulseConfig.LaserLow = np.uint32(int(float(self.txtLowLevel.text()) * measurementManager.maxPower))
            pulseConfig.LaserHigh = np.uint32(int(float(self.txtHighLevel.text()) * measurementManager.maxPower))

            return pulseConfig
        except Exception:
            traceback.print_exc()

    def updateMicrowaveODMRConfig(self):
        config = self.createODMRMicrowaveConfig()
        self.measurementManager.updateMicrowaveODMRConfig(config)

    def createODMRMicrowaveConfig(self):
        current_trigger_mode = 1
        rf_power = float(self.txtRFPower.text())

        config = microwaveConfiguration(
            centerFreq=float(self.txtCenterFreq.text()),
            power=rf_power,
            powerSweepStart=rf_power,
            powerSweepStop=rf_power,
            startFreq=float(self.txtStartFreq.text()),
            stopFreq=float(self.txtStopFreq.text()),
            trigMode=current_trigger_mode)

        config.stepSize = (config.stopFreq - config.startFreq) / int(self.txtCountNumber.text())
        config.stepTime = float(self.txtCountDuration.text()) / constConvertMicroSecondToMilisecond

        return config

    def updateMicrowaveRabiConfig(self):
        config = self.createRabiMicrowaveConfig()
        self.measurementManager.updateMicrowaveRabiConfig(config)

    def createRabiMicrowaveConfig(self):
        current_trigger_mode = 0
        rf_power = float(self.txtRFPowerRabi.text())

        config = microwaveConfiguration(
            centerFreq=float(self.txtCenterFreq.text()),
            power=rf_power,
            trigMode=current_trigger_mode)

        return config

    # Plot Methods
    def refreshPlot(self):
        type = self.getCurrentMeasurementTab()

        if type == measurementType.ODMR and self.measurementManager.getHaveODMRData():
            self.plotODMRData(self.measurementManager.getODMRData())
        elif type == measurementType.RabiPulse and self.measurementManager.getHaveRabiData():
            self.plotRabiData(self.measurementManager.getRabiData())

    def plotODMRData(self, data):
        try:
            # reset toolbar
            self.ODMRToolbar.home()
            self.ODMRToolbar.update()

            # reset plot
            self.axesODMR.clear()
            # self.axes2.clear()
            self.axesODMR.grid()

            x_label = self.measurementManager.ODMRXAxisLabel
            y_label = self.measurementManager.ODMRYAxisLabel

            # plot
            self.curveODMR, = self.axesODMR.plot(data[x_label], data[y_label], linewidth=0.5, c='black', label="Normalized signal")
            self.axesODMR.set_xlabel(x_label)
            self.axesODMR.set_ylabel(y_label)
            self.axesODMR.set_position([0.15, 0.15, 0.8, 0.8])
            self.axesODMR.legend(loc="upper right")
            
            self.odmrCanvas.draw()
        except Exception:
            traceback.print_exc()

    def plotRabiData(self, data):
        try:
            # reset toolbar
            self.rabiToolbar.home()
            self.rabiToolbar.update()

            # reset plot
            self.axesRabi1.clear()
            self.axesRabi2.clear()
            self.axesRabi1.grid()

            # plot
            xLabel = self.measurementManager.RabiXAxisLabel
            yLabel = self.measurementManager.RabiYAxisLabel

            self.curveRabi1 = self.axesRabi1.scatter(data[xLabel], data[yLabel], s=1, c='black')
            self.curveRabi2 = self.axesRabi1.plot(data[xLabel], data[yLabel], linewidth=0.5, c='black')
            
            self.axesRabi1.set_xlabel(xLabel)
            self.axesRabi1.set_ylabel(yLabel)
            
            self.axesRabi1.set_position([0.15, 0.15, 0.8, 0.8])
            self.rabiCanvas.draw()
        except Exception:
            traceback.print_exc()

    # Event Handler
    def connectionErrorEventHandler(self, error):
        try:
            QMessageBox.information(self, 'PLL', 'Error: %s.' % error)
            self.btnConnectRedPitaya.setText('Connect')
            self.btnConnectRedPitaya.setEnabled(True)
        except Exception:
            traceback.print_exc()
    
    def laserStatusChangedEventHandler(self):
        if self.measurementManager.getIsLaserOpen():
            self.btnOpenCloseAOM.setText('Close')
        else:
            self.btnOpenCloseAOM.setText('Open')

    def redPitayaConnectedHandler(self):
        try:
            self.btnConnectRedPitaya.setText('Disconnect')
            self.btnConnectRedPitaya.setEnabled(True)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def reciveODMRDataHandler(self, data, count):
        self.lblCurrentRepetetion.setText(str(count))
        self.plotODMRData(data)

    def reciveRabiDataHandler(self, data):
        # self.lblCurrentRepetetion.setText(str(count))
        self.plotRabiData(data)
    
    # TODO: Test
    def microwaveStatusChanged(self):
        try:
            if self.measurementManager.getIsMicrowaveConnected():
                self.indicateMicrowaveIsConnected()
            else:
                self.indicateMicrowaveIsDisconnected()
                return

            if self.measurementManager.getIsMicrowaveOn():
                self.indicateMicrowaveIsOn()

                type = self.getCurrentMeasurementTab()

                if type == measurementType.ODMR:
                    self.updateMicrowaveODMRConfig()
                elif type == measurementType.RabiPulse:
                    self.updateMicrowaveRabiConfig()
            else:
                self.indicateMicrowaveIsOff()
        except Exception as ex:
            print('Error in sending command to windfreak', ex)
            traceback.print_exc()

    #TODO: Rewrite to make sense...
    # def startRabiScan(self):
    #     try:
    #         if self.scan_idle:
    #             self.scan_idle = False
    #             self.btnScanRabi.setText('Stop')

    #             if self.lblCurrentValue.text() == '':
    #                 self.lblCurrentValue.setText(str(self.Range[0]))
    #                 self.CurrentIteration = 0
    #                 self.lblCurrentIterations.setText(str(self.CurrentIteration) + r'/' + str(self.Iterations))
    #                 print(self.lblCurrentIterations.text().split("/")[0])
    #                 self.ScanStatus = True
    #             else:
    #                 self.CurrentIteration = self.CurrentIteration + 1
    #                 self.lblCurrentIterations.setText(str(self.CurrentIteration) + r'/' + str(self.Iterations))
    #                 if int(self.CurrentIteration) > int(self.Iterations):
    #                     self.lblCurrentValue.setText(str(float(self.lblCurrentValue.text()) + self.Step))
    #                     self.CurrentIteration = 1
    #                     self.lblCurrentIterations.setText(str(self.CurrentIteration) + r'/' + str(self.Iterations))

    #             if self.cmbScanParam.currentIndex() == 0:
    #                 self.txtWidthMW.setText(str(self.lblCurrentValue.text()))

    #             self.txtParamValue.setText(str(self.lblCurrentValue.text()))

    #             if float(self.lblCurrentValue.text()) >= float(self.Range[-1]):
    #                 self.ScanStatus = False
    #                 self.lblCurrentValue.setText('')
    #                 self.scan_idle = True
    #                 self.btnScanRabi.setText('Scan')
    #             if self.ScanStatus:
    #                 self.clearAndStartRabiMeasurment()
    #         else:
    #             self.lblCurrentValue.setText('')
    #             self.lblCurrentIterations.setText('')
    #             self.ScanStatus = False
    #             self.scan_idle = True
    #             self.btnScanRabi.setText('Scan')
    #             self.save()
    #     except Exception:
    #         traceback.print_exc()

app = QApplication(sys.argv)
window = PhaseLockedLoop()
window.show()
sys.exit(app.exec_())
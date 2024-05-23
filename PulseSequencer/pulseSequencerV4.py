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
from Interfaces.AutoSaver import AutoSaver

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from LogicManagers.measurementManager import measurementManager
from LogicManagers.MeasurementProcessor import MeasurementProcessor
from LogicManagers.scanManager import scanManager
from LogicManagers import pulseAnalayzer

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
        self.measurementManager = measurementManager()
        self.measurementProcessor = MeasurementProcessor()
        self.dataSaver = dataSaver(self.measurementManager, measurementProcessor = self.measurementProcessor)
        self.scanManager = scanManager(self.measurementManager)
        self.autoSaver = AutoSaver(10)

        self.txtIPRedPitaya.setText(str(self.measurementManager.redPitaya.ip))
        self.txtPortRedPitaya.setText(str(self.measurementManager.redPitaya.port))

        self.txtIPPulseBlaster.setText(str(self.measurementManager.pulseBlaster.server_ip))
        self.txtPortPulseBlaster.setText(str(self.measurementManager.pulseBlaster.server_port))
        self.repetitionComboBox.addItems([m.name for m in repetition])

        # Register Events
        self.measurementManager.AOMStatusChangedEvent.connect(self.laserStatusChangedEventHandler)
        self.measurementManager.rabiPulseDataRecivedEvent.connect(self.reciveRabiDataHandler)
        self.measurementManager.ODMRDataRecivedEvent.connect(self.measurementProcessor.reciveODMRDataHandler)
        self.measurementManager.ODMRDataRecivedEvent.connect(self.reciveODMRDataHandler)
        self.measurementManager.connectionErrorEvent.connect(self.connectionErrorEventHandler)
        self.measurementManager.microwaveStatusChangeEvent.connect(self.microwaveStatusChanged)

        # self.autoSaver.autoSaveEvent.connect(self.saveODMR)
        self.measurementProcessor.photonsAVGRecivedEvent.connect(self.recivePhotonsAVGHandler)

        self.scanManager.rabiPulseEndedEvent.connect(self.scanUpdatedEventHandler)
        self.scanManager.errorEvent.connect(self.connectionErrorEventHandler)

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
        self.ODMRPathTextBox.setText(self.dataSaver.getODMRFolderToSave())
        self.ODMRFileNumber.setText(str(self.dataSaver.ODMRIndex))

        # rabi
        self.btnMeasureRabiPulse.clicked.connect(self.clearAndStartRabiMeasurement)
        self.connectMicrowaveRabiButton.clicked.connect(self.microwaveDeviceConnectionToggle)
        self.onOffRabiConnectButton.clicked.connect(self.microwaveOnOffToggle)
        self.btnSaveRabi.clicked.connect(self.saveRabi)
        self.rabiPathTextBox.setText(self.dataSaver.getRabiFolderToSave())
        self.rabiFileNumber.setText(str(self.dataSaver.rabiIndex))

        # scan
        self.btnScan.clicked.connect(self.clearAndStartScan)
        self.txtScanStart.setText('0')
        self.txtScanStop.setText('2')
        self.txtScanTimestep.setText('0.01')

        # initialize axes
        self.initializeODMRAxes()
        self.initializeRabiAxes()
        self.initializeScanAxes()

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
        figure, (self.axesRabi_complete, self.axesRabi_overlap) = plt.subplots(nrows=2, ncols=1)
        figure.set_facecolor('none')

        self.rabiCanvas = FigureCanvas(figure)
        self.rabiPulsePlotLayout.addWidget(self.rabiCanvas)

        # Create navigation toolbar
        self.rabiToolbar = NavigationToolbar(self.rabiCanvas, self.rabiPulsePlotWidget, False)

        # Remove subplots action
        actions = self.rabiToolbar.actions()
        self.rabiToolbar.removeAction(actions[7])
        self.rabiPulsePlotLayout.addWidget(self.rabiToolbar)

    def initializeScanAxes(self):
        # Create figure
        figure, self.axesScan = plt.subplots()
        figure.set_facecolor('none')

        self.scanCanvas = FigureCanvas(figure)
        self.scanPlotLayout.addWidget(self.scanCanvas)

        # Create navigation toolbar
        self.scanToolbar = NavigationToolbar(self.scanCanvas, self.scanPlotWidget, False)

        # Remove subplots action
        actions = self.scanToolbar.actions()
        self.scanToolbar.removeAction(actions[7])
        self.scanPlotLayout.addWidget(self.scanToolbar)

    # Getters
    def getCurrentMeasurementTab(self):
        if self.measurmentTabs.currentIndex() == measurementType.ODMR.value:
            return measurementType.ODMR
        # TODO: need to change to more options not related to the tabs...
        else:
            return measurementType.RabiPulse

    # Action Methods
    def laserOpenCloseToggle(self):
        try:
            config = self.createPulseConfiguration()
            self.measurementManager.laserOpenCloseToggle(config)
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
                self.btnConnectRedPitaya.setText('Disconnect')
            else:
                self.btnConnectRedPitaya.setText('Connect')
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
            microwave_config = self.createODMRMicrowaveConfig()
            pulse_config = self.createPulseConfiguration()
            repeat = repetition[self.repetitionComboBox.currentText()]

            max_repetitions = self.txtRepetitionMax.text()

            if max_repetitions == "":
                max_repetitions = None
            else:
                max_repetitions = int(max_repetitions)

            self.measurementManager.startNewODMRMeasurementAsync(pulse_config, microwave_config, repeat, max_repetitions)
            # self.measurementManager.startNewODMRMeasurement(pulse_config, microwave_config, repeat, max_repetitions)
            self.measurementProcessor.startPhotonsMeasurement()

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
            self.measurementManager.startNewRabiPulseMeasurementAsync(pulse_config, microwave_config)
        except Exception:
            traceback.print_exc()

    def clearAndStartScan(self):
        try:
            microwave_config = self.createRabiMicrowaveConfig()
            pulse_config = self.createPulseConfiguration()
            start_time = float(self.txtScanStart.text())
            stop_time = float(self.txtScanStop.text())
            time_step = float(self.txtScanTimestep.text())
            
            self.scanManager.startScanAsync(pulse_config, microwave_config, 
                                                   start_time, stop_time, time_step)
        except Exception as ex:
            print(ex)
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

    # TODO: Test
    def saveODMR(self):
        try:
            self.dataSaver.setODMRFolderToSave(self.ODMRPathTextBox.text())
            comment = self.ODMRComment.text()

            self.dataSaver.saveODMR(comment, self.ODMRFileNumber.text())      
            self.dataSaver.savePhotonsAVG(self.ODMRFileNumber.text())
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    # TODO: Test
    def saveRabi(self):
        try:
            self.dataSaver.setRabiFolderToSave(self.rabiPathTextBox.text())
            comment = self.rabiCommentTextBox.text()

            self.dataSaver.saveRabiPulse(comment, self.rabiFileNumber.text())      
            self.rabiFileNumber.setText(str(self.dataSaver.rabiIndex))
        except Exception as ex:
            print(ex)
            traceback.print_exc()
        pass 

    # Config Methods
    def createPulseConfiguration(self):
        try:
            pulseConfig = pulseConfiguration()

            pulseConfig.measurement_type = self.getCurrentMeasurementTab()
                 
            if pulseConfig.measurement_type == measurementType.ODMR:
                pulseConfig.count_duration = int(self.txtCountDuration.text())
            else:
                pulseConfig.count_duration = 1

            pulseConfig.samples_number = float(self.txtCountNumber.text())
            pulseConfig.threshold = float(self.txtThreshold.text())
            pulseConfig.iterations = int(self.txtAveragesNumber.text())
            pulseConfig.pump_start = float(self.txtStartPump.text())
            pulseConfig.pump_duration = float(self.txtWidthPump.text())
            pulseConfig.microwave_start = float(self.txtStartMW.text())
            pulseConfig.microwave_duration = float(self.txtWidthMW.text())
            pulseConfig.image_start = float(self.txtStartImage.text())
            pulseConfig.image_duration = float(self.txtWidthImage.text())
            pulseConfig.readout_start = float(self.txtStartReadout.text())
            pulseConfig.low_voltage_AOM = float(self.txtLowLevel.text())
            pulseConfig.high_voltage_AOM = float(self.txtHighLevel.text())

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
            self.axesODMR.grid()

            x_label = data.columns[0]
            y_label = data.columns[1]

            # plot
            self.curveODMR, = self.axesODMR.plot(data[x_label], data[y_label], linewidth=0.5, c='black', label="Normalized signal")
            self.axesODMR.set_xlabel(x_label)
            self.axesODMR.set_ylabel(y_label)
            self.axesODMR.set_position([0.15, 0.15, 0.8, 0.8])
            self.axesODMR.legend(loc="upper right")
            
            self.odmrCanvas.draw()
        except Exception:
            traceback.print_exc()

    def plotPhotonsAVG(self, photonsAVG):
        self.photonsCountLabel.setText(str(photonsAVG))
        self.photonsCountLabel_big.setText(str(photonsAVG))

    def plotRabiData(self, data):
        try:
            # reset toolbar
            self.rabiToolbar.home()
            self.rabiToolbar.update()


            # plot
            self.plotRabiCompletePulse(data)
            self.plotRabiOverlapPulses(data)

            self.rabiCanvas.draw()
        except Exception:
            traceback.print_exc()

    def plotRabiCompletePulse(self, data):
        axes = self.axesRabi_complete 
        xLabel = self.measurementManager.RabiXAxisLabel
        yLabel = self.measurementManager.RabiYAxisLabel

        # reset plot
        axes.clear()
        axes.grid()

        self.curveRabi1 = axes.scatter(data[xLabel], data[yLabel], s=1, c='black')
        self.curveRabi2 = axes.plot(data[xLabel], data[yLabel], linewidth=0.5, c='black')
        
        axes.set_xlabel(xLabel)
        axes.set_ylabel(yLabel)
        
        # axes.set_position([0.15, 0.15, 0.8, 0.8])

    def plotRabiOverlapPulses(self, data):
        axes = self.axesRabi_overlap 
        xLabel = self.measurementManager.RabiXAxisLabel
        yLabel = self.measurementManager.RabiYAxisLabel

        # reset plot
        axes.clear()
        axes.grid()

        t_image, y_image = pulseAnalayzer.getOnlyImage(data[xLabel], data[yLabel])
        t_pump, y_pump = pulseAnalayzer.getOnlyPump(data[xLabel], data[yLabel])

        axes.plot(t_pump, y_pump, label = "Pump")
        axes.plot(t_image, y_image, label = "Image")
        
        axes.legend()

        axes.set_xlabel(xLabel)
        axes.set_ylabel(yLabel)

    def plotScan(self, time, points):
        # reset toolbar
        self.scanToolbar.home()
        self.scanToolbar.update()

        # reset plot
        self.axesScan.clear()
        self.axesScan.grid()

        x_label = "Time [micro second]"
        y_label = "Image Intensity (arbitrary units)"

        # plot
        self.curveODMR, = self.axesScan.plot(time, points, linewidth=0.5, c='black')
        self.axesScan.set_xlabel(x_label)
        self.axesScan.set_ylabel(y_label)
        self.axesScan.set_position([0.15, 0.15, 0.8, 0.8])
        
        self.scanCanvas.draw()

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

    def reciveODMRDataHandler(self, data, count):
        self.lblCurrentRepetetion.setText(str(count))
        self.plotODMRData(data)
        # self.autoSaver.onData()

    def recivePhotonsAVGHandler(self, photonsAVG):
        self.plotPhotonsAVG(photonsAVG)

    def reciveRabiDataHandler(self, data):
        # self.lblCurrentRepetetion.setText(str(count))
        self.plotRabiData(data)

    def scanUpdatedEventHandler(self, point, time):
        self.plotScan(self.scanManager.extractedData_dima.keys(), self.scanManager.extractedData_dima.values())
        
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

app = QApplication(sys.argv)
window = PhaseLockedLoop()
window.show()
sys.exit(app.exec_())
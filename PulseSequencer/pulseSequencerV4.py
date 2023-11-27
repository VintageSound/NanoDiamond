import numpy as np
import sys
import traceback
import time

from Data.pulseConfiguration import pulseConfiguration
from Data.microwaveConfiguration import microwaveConfiguration

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtTest

import matplotlib

from Data.MeasurmentType import MeasurmentType

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from LogicManagers.measurmentManager import measurmentManager

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) # enable high-dpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) # use high-dpi icons

Ui_PhaseLockedLoop, QMainWindow = uic.loadUiType('PulseSequencer\PulseSequencerV4.ui')

constConvertMicroSecondToMilisecond = 1000

class PhaseLockedLoop(QMainWindow, Ui_PhaseLockedLoop):    
    def __init__(self):
        super(PhaseLockedLoop, self).__init__()
        self.setupUi(self)
        self.measurmentManager = measurmentManager(self)

        self.txtIP.setText(str(self.measurmentManager.redPitaya.ip))
        self.txtPort.setText(str(self.measurmentManager.redPitaya.port))

        # Register Events
        self.measurmentManager.registerToAOMStatusChangedEvent(self.laserStatusChangedEventHandler)
        self.measurmentManager.registerToRedPitayaConnectedEvent(self.redPitayaConnectedHandler)
        
        self.measurmentManager.registerToRabiPulseDataRecivedEvent(self.reciveRabiDataHandler)
        self.measurmentManager.registerToODMRDataRecivedEvent(self.reciveODMRDataHandler)
        self.measurmentManager.registerConnectionErrorEvent(self.connectionErrorEventHandler)

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
        self.btnSave.clicked.connect(self.save)
        self.btnOpen.clicked.connect(self.laserOpenCloseToggle)
        self.btnConnect_2.clicked.connect(self.microwaveDeviceConnectionToggle)
        self.btnOn_Off.clicked.connect(self.microwaveOnOffToggle)
        
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
        self.comboBoxMode.setCurrentIndex(0)
        self.btnOn_Off.setText("RF is Off")
        # Declare operation mode
        self.comboBoxMeasureType.addItems([m.name for m in MeasurmentType])
        self.comboBoxMeasureType.setCurrentIndex(0)
        # set SynthHD as default MW device
        self.comboBoxMWdevice.setCurrentIndex(0)
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
        self.txtPath.setText(self.measurmentManager.dataSaver.getFolderToSave())
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
        # self.txtLowLevel.textChanged.connect(self.configurePulseSequence)
        self.txtHighLevel.setText('0.9')
        # self.txtHighLevel.textChanged.connect(self.configurePulseSequence)
    
    # Action Methods
    def applyChangesOfMicrowaveSettings(self):
        try:
            self.updateMicrowaveSweepConfig()

            if self.measurmentManager.measurmentType == MeasurmentType.ODMR:
                self.plotODMRData()            
            elif self.measurmentManager.measurmentType == MeasurmentType.SingleRabiPulse:
                self.plotRabiData()                           
        except Exception:
            traceback.print_exc()

    def laserOpenCloseToggle(self):
        try:
            self.measurmentManager.laserOpenCloseToggle()
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def microwaveDeviceConnectionToggle(self):
        try:
            self.measurmentManager.microwaveDeviceConnectionToggle()

            if self.measurmentManager.isMicrowaveOpen():
                self.btnOn_Off.setText("RF is off")
                self.btnOn_Off.setStyleSheet("background-color:none")
                self.btnConnect_2.setText('Connect')
            else:
                self.btnOn_Off.setText("RF is On")
                self.btnOn_Off.setStyleSheet("background-color:red")
                self.btnConnect_2.setText('Disconnect')
        except Exception as ex:
            print('Cannot connect to windfreak', ex)
            traceback.print_exc()

    def microwaveOnOffToggle(self):
        try:
            self.measurmentManager.microwaveOnOffToggle()

            if self.measurmentManager.isMicrowaveOn():
                self.btnOn_Off.setText("RF is On")
                self.btnOn_Off.setStyleSheet("background-color:red")
            else:
                self.btnOn_Off.setText("RF is off")
                self.btnOn_Off.setStyleSheet("background-color:none")

        except Exception:
            print('Error in sending command to windfreak')
            traceback.print_exc()

    def connectToRedPitayaToggle(self):
        try:
            self.measurmentManager.connectToRedPitayaToggle(self.txtIP.text(), int(self.txtPort.text()))

            if self.measurmentManager.isRedPitayaConnected():
                # Wait for connection event to enable the button  
                self.btnConnect.setEnabled(False)
            else:
                self.btnConnect.setText('Connect')
                self.btnConnect.setEnabled(True)

            # Connect also to pulse blaster... TODO: change to differebt button
            self.measurmentManager.connectToPulseBlaster()
        except Exception:
            traceback.print_exc()

    def clearAndStartODMR(self):
        try:
            self.lblRepeatNum.setText('')
            self.updateMicrowaveSweepConfig()
            config = self.createPulseConfiguration()
            self.measurmentManager.startNewODMRMeasuremnt(config)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def clearAndStartRabiMeasurment(self):
        try:
            config = self.createPulseConfiguration()
            self.measurmentManager.startNewRabiPulseMeasuremnt(config)
        except Exception:
            traceback.print_exc()

    def save(self):
        try:
            if self.measurmentManager.measurmentType == MeasurmentType.ODMR:
                self.saveODMR()
            elif self.measurmentManager.measurmentType == MeasurmentType.SingleRabiPulse:
                self.saveRabi()
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    # Config Methods
    def createPulseConfiguration(self):
        try:
            timeStep = measurmentManager.redPitayaTimeStep
            pulseConfig = pulseConfiguration()

            # TODO: regard ramsi and multipule rabi when needed
            if self.measurmentManager.measurmentType == MeasurmentType.ODMR:
                pulseConfig.CountDuration = np.uint32(int(float(self.txtCountDuration.text()) / timeStep))
            else:
                pulseConfig.CountDuration = np.uint32(1)

            pulseConfig.CountNumber = np.uint32(int(np.log2(float(self.txtCountNumber.text()))))
            pulseConfig.Threshold = np.uint32(int(float(self.txtThreshold.text()) * measurmentManager.maxPower / 20)) # why 20 ????
            pulseConfig.AveragesNumber = np.uint32(int(self.txtAveragesNumber.text()))
            pulseConfig.StartPump = np.uint32(int(float(self.txtStartPump.text()) / timeStep))
            pulseConfig.WidthPump = np.uint32(int(float(self.txtWidthPump.text()) / timeStep))
            pulseConfig.StartMW = np.uint32(int(float(self.txtStartMW.text()) / timeStep))
            pulseConfig.WidthMW = np.uint32(int(float(self.txtWidthMW.text()) / timeStep))
            pulseConfig.StartImage = np.uint32(int(float(self.txtStartImage.text()) / timeStep))
            pulseConfig.WidthImage = np.uint32(int(float(self.txtWidthImage.text()) / timeStep))
            pulseConfig.StartReadout = np.uint32(int(float(self.txtStartReadout.text()) / timeStep))
            pulseConfig.LaserLow = np.uint32(int(float(self.txtLowLevel.text()) * measurmentManager.maxPower))
            pulseConfig.LaserHigh = np.uint32(int(float(self.txtHighLevel.text()) * measurmentManager.maxPower))

            return pulseConfig
        except Exception:
            traceback.print_exc()

    def updateMicrowaveSweepConfig(self):
        config = microwaveConfiguration(
            centerFreq=float(self.txtCenterFreq.text()), 
            power=float(self.txtRFPower.text()), 
            powerSweepStart=float(self.txtRFPower.text()),
            powerSweepEnd=float(self.txtRFPower.text()),
            startFreq=float(self.txtStartFreq.text()),
            stopFreq=float(self.txtStopFreq.text()),
            trigMode=self.comboBoxMode.currentIndex()
            )

        config.stepSize = (config.StopFreq - config.StartFreq) / int(self.txtCountNumber.text())
        config.stepTime = float(self.txtCountDuration.text()) / constConvertMicroSecondToMilisecond # convert from micro seconds to ms

        self.measurmentManager.updateMicrowaveSweepConfig(config)
    
    # Plot Methods
    def plotODMRData(self, data):
        try:
            # reset toolbar
            self.toolbar.home()
            self.toolbar.update()

            # reset plot
            self.axes.clear()
            self.axes2.clear()
            self.axes.grid()

            xLabel = self.measurmentManager.ODMRXAxisLabel
            yLabel = self.measurmentManager.ODMRYAxisLabel

            # plot
            self.curve_3_2, = self.axes.plot(data[xLabel], self.ODMRData[yLabel], linewidth=0.5, c='black', label="Normalized signal")
            self.axes.set_xlabel(xLabel)
            self.axes.set_ylabel(yLabel)
            self.axes.set_position([0.15, 0.15, 0.8, 0.8])
            self.axes.legend(loc="upper right")
            
            self.canvas.draw()
        except Exception:
            traceback.print_exc()

    def plotRabiData(self, data):
        try:
            # reset toolbar
            self.toolbar.home()
            self.toolbar.update()

            # reset plot
            self.axes.clear()
            self.axes2.clear()
            self.axes.grid()

            # plot
            xLabel = self.measurmentManager.RabiXAxisLabel
            yLabel = self.measurmentManager.RabiYAxisLabel

            self.curve_3_1 = self.axes.scatter(data[xLabel], self.RabiData[yLabel], s=1, c='black')
            self.curve_3_2 = self.axes.plot(data[xLabel], self.RabiData[yLabel], linewidth=0.5, c='black')
            
            self.axes.set_xlabel(xLabel)
            self.axes.set_ylabel(yLabel)
            
            self.axes.set_position([0.15, 0.15, 0.8, 0.8])
            self.canvas.draw()
        except Exception:
            traceback.print_exc()

    # Event Handler
    def connectionErrorEventHandler(self, error):
        try:
            QMessageBox.information(self, 'PLL', 'Error: %s.' % error)
            self.btnConnect.setText('Connect')
            self.btnConnect.setEnabled(True)
        except Exception:
            traceback.print_exc()
    
    def laserStatusChangedEventHandler(self):
        if self.measurmentManager.isLaserOpen():
            self.btnOpen.setText('Close')
        else:
            self.btnOpen.setText('Open')

    def redPitayaConnectedHandler(self):
        try:
            self.btnConnect.setText('Disconnect')
            self.btnConnect.setEnabled(True)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def reciveODMRDataHandler(self, data):
        self.plotODMRData(data)

        self.btnStart.setEnabled(True)
        self.btnConnect.setText('Connect')

    def reciveRabiDataHandler(self, data):
        self.plotRabiData(data)

        self.btnStart.setEnabled(True)
        self.btnConnect.setText('Connect')

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
    def path_changed(self):
        self.txtNum.setText(r'0')

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
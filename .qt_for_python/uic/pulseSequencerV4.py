# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulseSequencerV4.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_odmr(object):
    def setupUi(self, odmr):
        if not odmr.objectName():
            odmr.setObjectName(u"odmr")
        odmr.resize(1312, 1117)
        odmr.setMinimumSize(QSize(0, 0))
        odmr.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget = QWidget(odmr)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(800, 600))
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalWidget = QWidget(self.centralwidget)
        self.verticalWidget.setObjectName(u"verticalWidget")
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamilies([u"Tahoma"])
        self.verticalWidget.setFont(font)
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalWidget = QWidget(self.verticalWidget)
        self.horizontalWidget.setObjectName(u"horizontalWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.horizontalWidget.sizePolicy().hasHeightForWidth())
        self.horizontalWidget.setSizePolicy(sizePolicy1)
        self.horizontalWidget.setMinimumSize(QSize(0, 100))
        self.horizontalLayout = QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.PulseBlaster = QGroupBox(self.horizontalWidget)
        self.PulseBlaster.setObjectName(u"PulseBlaster")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.PulseBlaster.sizePolicy().hasHeightForWidth())
        self.PulseBlaster.setSizePolicy(sizePolicy2)
        self.PulseBlaster.setMinimumSize(QSize(380, 100))
        font1 = QFont()
        font1.setFamilies([u"Calibri Light"])
        font1.setPointSize(12)
        font1.setBold(False)
        self.PulseBlaster.setFont(font1)
        self.PulseBlaster.setFlat(False)
        self.PulseBlaster.setCheckable(False)
        self.lblPortPulseBlaster = QLabel(self.PulseBlaster)
        self.lblPortPulseBlaster.setObjectName(u"lblPortPulseBlaster")
        self.lblPortPulseBlaster.setGeometry(QRect(20, 60, 111, 16))
        self.lblPortPulseBlaster.setFont(font1)
        self.btnConnectPulseBlaster = QPushButton(self.PulseBlaster)
        self.btnConnectPulseBlaster.setObjectName(u"btnConnectPulseBlaster")
        self.btnConnectPulseBlaster.setGeometry(QRect(260, 30, 101, 51))
        self.txtPortPulseBlaster = QLineEdit(self.PulseBlaster)
        self.txtPortPulseBlaster.setObjectName(u"txtPortPulseBlaster")
        self.txtPortPulseBlaster.setGeometry(QRect(72, 60, 171, 20))
        self.txtIPPulseBlaster = QLineEdit(self.PulseBlaster)
        self.txtIPPulseBlaster.setObjectName(u"txtIPPulseBlaster")
        self.txtIPPulseBlaster.setGeometry(QRect(72, 30, 171, 20))
        self.lblIPPulseBlaster = QLabel(self.PulseBlaster)
        self.lblIPPulseBlaster.setObjectName(u"lblIPPulseBlaster")
        self.lblIPPulseBlaster.setGeometry(QRect(20, 30, 91, 16))
        self.lblIPPulseBlaster.setFont(font1)

        self.horizontalLayout_4.addWidget(self.PulseBlaster)

        self.RedPitaya = QGroupBox(self.horizontalWidget)
        self.RedPitaya.setObjectName(u"RedPitaya")
        sizePolicy2.setHeightForWidth(self.RedPitaya.sizePolicy().hasHeightForWidth())
        self.RedPitaya.setSizePolicy(sizePolicy2)
        self.RedPitaya.setMinimumSize(QSize(380, 100))
        font2 = QFont()
        font2.setFamilies([u"Calibri Light"])
        font2.setPointSize(12)
        self.RedPitaya.setFont(font2)
        self.RedPitaya.setFlat(False)
        self.RedPitaya.setCheckable(False)
        self.lblPortRedPitaya = QLabel(self.RedPitaya)
        self.lblPortRedPitaya.setObjectName(u"lblPortRedPitaya")
        self.lblPortRedPitaya.setGeometry(QRect(20, 60, 111, 16))
        self.lblPortRedPitaya.setFont(font2)
        self.btnConnectRedPitaya = QPushButton(self.RedPitaya)
        self.btnConnectRedPitaya.setObjectName(u"btnConnectRedPitaya")
        self.btnConnectRedPitaya.setGeometry(QRect(260, 30, 101, 51))
        self.txtPortRedPitaya = QLineEdit(self.RedPitaya)
        self.txtPortRedPitaya.setObjectName(u"txtPortRedPitaya")
        self.txtPortRedPitaya.setGeometry(QRect(62, 60, 181, 20))
        self.txtIPRedPitaya = QLineEdit(self.RedPitaya)
        self.txtIPRedPitaya.setObjectName(u"txtIPRedPitaya")
        self.txtIPRedPitaya.setGeometry(QRect(62, 30, 181, 20))
        self.lblIPRedPitaya = QLabel(self.RedPitaya)
        self.lblIPRedPitaya.setObjectName(u"lblIPRedPitaya")
        self.lblIPRedPitaya.setGeometry(QRect(20, 30, 91, 16))
        self.lblIPRedPitaya.setFont(font2)

        self.horizontalLayout_4.addWidget(self.RedPitaya)

        self.LaserControl = QGroupBox(self.horizontalWidget)
        self.LaserControl.setObjectName(u"LaserControl")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.LaserControl.sizePolicy().hasHeightForWidth())
        self.LaserControl.setSizePolicy(sizePolicy3)
        self.LaserControl.setMinimumSize(QSize(380, 100))
        self.LaserControl.setFont(font2)
        self.lblLowLevel = QLabel(self.LaserControl)
        self.lblLowLevel.setObjectName(u"lblLowLevel")
        self.lblLowLevel.setGeometry(QRect(30, 30, 101, 16))
        self.lblHighLevel = QLabel(self.LaserControl)
        self.lblHighLevel.setObjectName(u"lblHighLevel")
        self.lblHighLevel.setGeometry(QRect(30, 60, 101, 20))
        self.txtLowLevel = QLineEdit(self.LaserControl)
        self.txtLowLevel.setObjectName(u"txtLowLevel")
        self.txtLowLevel.setGeometry(QRect(110, 30, 141, 20))
        self.txtHighLevel = QLineEdit(self.LaserControl)
        self.txtHighLevel.setObjectName(u"txtHighLevel")
        self.txtHighLevel.setGeometry(QRect(110, 60, 141, 20))
        self.btnOpenCloseAOM = QPushButton(self.LaserControl)
        self.btnOpenCloseAOM.setObjectName(u"btnOpenCloseAOM")
        self.btnOpenCloseAOM.setGeometry(QRect(270, 30, 91, 51))

        self.horizontalLayout_4.addWidget(self.LaserControl)


        self.horizontalLayout.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.horizontalWidget)

        self.plotWidget = QWidget(self.verticalWidget)
        self.plotWidget.setObjectName(u"plotWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.plotWidget.sizePolicy().hasHeightForWidth())
        self.plotWidget.setSizePolicy(sizePolicy4)
        self.plotWidget.setMinimumSize(QSize(0, 0))
        self.plotLayout = QVBoxLayout(self.plotWidget)
        self.plotLayout.setObjectName(u"plotLayout")
        self.measurmentTabs = QTabWidget(self.plotWidget)
        self.measurmentTabs.setObjectName(u"measurmentTabs")
        self.ODMRTab = QWidget()
        self.ODMRTab.setObjectName(u"ODMRTab")
        self.gridLayout_4 = QGridLayout(self.ODMRTab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalWidget_2 = QWidget(self.ODMRTab)
        self.verticalWidget_2.setObjectName(u"verticalWidget_2")
        sizePolicy3.setHeightForWidth(self.verticalWidget_2.sizePolicy().hasHeightForWidth())
        self.verticalWidget_2.setSizePolicy(sizePolicy3)
        self.gridLayout = QGridLayout(self.verticalWidget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ODMR = QGroupBox(self.verticalWidget_2)
        self.ODMR.setObjectName(u"ODMR")
        sizePolicy1.setHeightForWidth(self.ODMR.sizePolicy().hasHeightForWidth())
        self.ODMR.setSizePolicy(sizePolicy1)
        self.ODMR.setMinimumSize(QSize(450, 260))
        self.ODMR.setFont(font2)
        self.lblRepeatNum = QLabel(self.ODMR)
        self.lblRepeatNum.setObjectName(u"lblRepeatNum")
        self.lblRepeatNum.setGeometry(QRect(30, 120, 71, 16))
        self.formLayoutWidget = QWidget(self.ODMR)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 30, 431, 181))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lblCountDuration = QLabel(self.formLayoutWidget)
        self.lblCountDuration.setObjectName(u"lblCountDuration")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.lblCountDuration)

        self.txtCountDuration = QLineEdit(self.formLayoutWidget)
        self.txtCountDuration.setObjectName(u"txtCountDuration")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.txtCountDuration)

        self.lblCountNumber = QLabel(self.formLayoutWidget)
        self.lblCountNumber.setObjectName(u"lblCountNumber")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.lblCountNumber)

        self.txtCountNumber = QLineEdit(self.formLayoutWidget)
        self.txtCountNumber.setObjectName(u"txtCountNumber")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.txtCountNumber)

        self.lblThreshold = QLabel(self.formLayoutWidget)
        self.lblThreshold.setObjectName(u"lblThreshold")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.lblThreshold)

        self.txtThreshold = QLineEdit(self.formLayoutWidget)
        self.txtThreshold.setObjectName(u"txtThreshold")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.txtThreshold)

        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.txtRepetitionMax = QLineEdit(self.formLayoutWidget)
        self.txtRepetitionMax.setObjectName(u"txtRepetitionMax")

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.txtRepetitionMax)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.label_4)

        self.lblCurrentRepetetion = QLabel(self.formLayoutWidget)
        self.lblCurrentRepetetion.setObjectName(u"lblCurrentRepetetion")

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.lblCurrentRepetetion)

        self.repetitionComboBox = QComboBox(self.formLayoutWidget)
        self.repetitionComboBox.setObjectName(u"repetitionComboBox")

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.repetitionComboBox)

        self.btnStartODMR = QPushButton(self.ODMR)
        self.btnStartODMR.setObjectName(u"btnStartODMR")
        self.btnStartODMR.setGeometry(QRect(10, 220, 212, 28))
        self.btnStopODMR = QPushButton(self.ODMR)
        self.btnStopODMR.setObjectName(u"btnStopODMR")
        self.btnStopODMR.setGeometry(QRect(230, 220, 211, 28))

        self.gridLayout.addWidget(self.ODMR, 1, 0, 1, 1)

        self.MW = QGroupBox(self.verticalWidget_2)
        self.MW.setObjectName(u"MW")
        self.MW.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.MW.sizePolicy().hasHeightForWidth())
        self.MW.setSizePolicy(sizePolicy1)
        self.MW.setMinimumSize(QSize(450, 220))
        self.MW.setFont(font2)
        self.layoutWidget = QWidget(self.MW)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(18, 70, 421, 101))
        self.formLayout = QFormLayout(self.layoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.lblStartFreq = QLabel(self.layoutWidget)
        self.lblStartFreq.setObjectName(u"lblStartFreq")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lblStartFreq)

        self.txtStartFreq = QLineEdit(self.layoutWidget)
        self.txtStartFreq.setObjectName(u"txtStartFreq")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.txtStartFreq)

        self.lblStopFreq = QLabel(self.layoutWidget)
        self.lblStopFreq.setObjectName(u"lblStopFreq")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lblStopFreq)

        self.txtStopFreq = QLineEdit(self.layoutWidget)
        self.txtStopFreq.setObjectName(u"txtStopFreq")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.txtStopFreq)

        self.lblRFPower = QLabel(self.layoutWidget)
        self.lblRFPower.setObjectName(u"lblRFPower")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lblRFPower)

        self.txtRFPower = QLineEdit(self.layoutWidget)
        self.txtRFPower.setObjectName(u"txtRFPower")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.txtRFPower)

        self.comboBoxMWdevice = QComboBox(self.MW)
        self.comboBoxMWdevice.addItem("")
        self.comboBoxMWdevice.setObjectName(u"comboBoxMWdevice")
        self.comboBoxMWdevice.setGeometry(QRect(20, 30, 82, 26))
        self.comboBoxMWdevice.setAutoFillBackground(False)
        self.comboBoxMWdevice.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.connectMicrowaveODMRButton = QPushButton(self.MW)
        self.connectMicrowaveODMRButton.setObjectName(u"connectMicrowaveODMRButton")
        self.connectMicrowaveODMRButton.setGeometry(QRect(10, 180, 211, 28))
        self.onOffODMRConnectButton = QPushButton(self.MW)
        self.onOffODMRConnectButton.setObjectName(u"onOffODMRConnectButton")
        self.onOffODMRConnectButton.setGeometry(QRect(230, 180, 211, 28))

        self.gridLayout.addWidget(self.MW, 0, 0, 1, 1)

        self.DataSave = QGroupBox(self.verticalWidget_2)
        self.DataSave.setObjectName(u"DataSave")
        self.DataSave.setFont(font2)
        self.formLayoutWidget_2 = QWidget(self.DataSave)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(9, 22, 431, 151))
        self.formLayout_4 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lblPath = QLabel(self.formLayoutWidget_2)
        self.lblPath.setObjectName(u"lblPath")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.lblPath)

        self.ODMRPathTextBox = QLineEdit(self.formLayoutWidget_2)
        self.ODMRPathTextBox.setObjectName(u"ODMRPathTextBox")

        self.formLayout_4.setWidget(1, QFormLayout.SpanningRole, self.ODMRPathTextBox)

        self.lblParamValue = QLabel(self.formLayoutWidget_2)
        self.lblParamValue.setObjectName(u"lblParamValue")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.lblParamValue)

        self.ODMRFileNumber = QLineEdit(self.formLayoutWidget_2)
        self.ODMRFileNumber.setObjectName(u"ODMRFileNumber")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.ODMRFileNumber)

        self.lblComment = QLabel(self.formLayoutWidget_2)
        self.lblComment.setObjectName(u"lblComment")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.lblComment)

        self.ODMRComment = QLineEdit(self.formLayoutWidget_2)
        self.ODMRComment.setObjectName(u"ODMRComment")

        self.formLayout_4.setWidget(4, QFormLayout.SpanningRole, self.ODMRComment)

        self.btnSaveODMR = QPushButton(self.DataSave)
        self.btnSaveODMR.setObjectName(u"btnSaveODMR")
        self.btnSaveODMR.setGeometry(QRect(230, 180, 211, 51))

        self.gridLayout.addWidget(self.DataSave, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.verticalWidget_2, 0, 1, 1, 1)

        self.ODMRPlotWidget = QWidget(self.ODMRTab)
        self.ODMRPlotWidget.setObjectName(u"ODMRPlotWidget")
        self.ODMRPlotLayout = QGridLayout(self.ODMRPlotWidget)
        self.ODMRPlotLayout.setObjectName(u"ODMRPlotLayout")

        self.gridLayout_2.addWidget(self.ODMRPlotWidget, 0, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.measurmentTabs.addTab(self.ODMRTab, "")
        self.RabiPulseTab = QWidget()
        self.RabiPulseTab.setObjectName(u"RabiPulseTab")
        self.gridLayout_41 = QGridLayout(self.RabiPulseTab)
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.gridLayout_21.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalWidget_21 = QWidget(self.RabiPulseTab)
        self.verticalWidget_21.setObjectName(u"verticalWidget_21")
        sizePolicy3.setHeightForWidth(self.verticalWidget_21.sizePolicy().hasHeightForWidth())
        self.verticalWidget_21.setSizePolicy(sizePolicy3)
        self.gridLayout1 = QGridLayout(self.verticalWidget_21)
        self.gridLayout1.setObjectName(u"gridLayout1")
        self.MW1 = QGroupBox(self.verticalWidget_21)
        self.MW1.setObjectName(u"MW1")
        self.MW1.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.MW1.sizePolicy().hasHeightForWidth())
        self.MW1.setSizePolicy(sizePolicy1)
        self.MW1.setMinimumSize(QSize(450, 170))
        self.MW1.setFont(font2)
        self.comboBoxMWdeviceRabi = QComboBox(self.MW1)
        self.comboBoxMWdeviceRabi.addItem("")
        self.comboBoxMWdeviceRabi.setObjectName(u"comboBoxMWdeviceRabi")
        self.comboBoxMWdeviceRabi.setGeometry(QRect(20, 30, 82, 26))
        self.comboBoxMWdeviceRabi.setAutoFillBackground(False)
        self.comboBoxMWdeviceRabi.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.connectMicrowaveRabiButton = QPushButton(self.MW1)
        self.connectMicrowaveRabiButton.setObjectName(u"connectMicrowaveRabiButton")
        self.connectMicrowaveRabiButton.setGeometry(QRect(10, 130, 211, 28))
        self.onOffRabiConnectButton = QPushButton(self.MW1)
        self.onOffRabiConnectButton.setObjectName(u"onOffRabiConnectButton")
        self.onOffRabiConnectButton.setGeometry(QRect(230, 130, 211, 28))
        self.layoutWidget_2 = QWidget(self.MW1)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(10, 60, 431, 58))
        self.formLayout_7 = QFormLayout(self.layoutWidget_2)
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.formLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout_7.setContentsMargins(0, 0, 0, 0)
        self.lblCenterFreq = QLabel(self.layoutWidget_2)
        self.lblCenterFreq.setObjectName(u"lblCenterFreq")

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.lblCenterFreq)

        self.txtCenterFreq = QLineEdit(self.layoutWidget_2)
        self.txtCenterFreq.setObjectName(u"txtCenterFreq")

        self.formLayout_7.setWidget(0, QFormLayout.FieldRole, self.txtCenterFreq)

        self.lblRFPowerRabi = QLabel(self.layoutWidget_2)
        self.lblRFPowerRabi.setObjectName(u"lblRFPowerRabi")

        self.formLayout_7.setWidget(1, QFormLayout.LabelRole, self.lblRFPowerRabi)

        self.txtRFPowerRabi = QLineEdit(self.layoutWidget_2)
        self.txtRFPowerRabi.setObjectName(u"txtRFPowerRabi")

        self.formLayout_7.setWidget(1, QFormLayout.FieldRole, self.txtRFPowerRabi)


        self.gridLayout1.addWidget(self.MW1, 0, 0, 1, 1)

        self.DataSave1 = QGroupBox(self.verticalWidget_21)
        self.DataSave1.setObjectName(u"DataSave1")
        self.DataSave1.setFont(font2)
        self.formLayoutWidget_21 = QWidget(self.DataSave1)
        self.formLayoutWidget_21.setObjectName(u"formLayoutWidget_21")
        self.formLayoutWidget_21.setGeometry(QRect(9, 22, 431, 151))
        self.formLayout_41 = QFormLayout(self.formLayoutWidget_21)
        self.formLayout_41.setObjectName(u"formLayout_41")
        self.formLayout_41.setContentsMargins(0, 0, 0, 0)
        self.lblPath1 = QLabel(self.formLayoutWidget_21)
        self.lblPath1.setObjectName(u"lblPath1")

        self.formLayout_41.setWidget(0, QFormLayout.LabelRole, self.lblPath1)

        self.rabiPathTextBox = QLineEdit(self.formLayoutWidget_21)
        self.rabiPathTextBox.setObjectName(u"rabiPathTextBox")

        self.formLayout_41.setWidget(1, QFormLayout.SpanningRole, self.rabiPathTextBox)

        self.lblParamValue1 = QLabel(self.formLayoutWidget_21)
        self.lblParamValue1.setObjectName(u"lblParamValue1")

        self.formLayout_41.setWidget(2, QFormLayout.LabelRole, self.lblParamValue1)

        self.ODMRFileNumber_2 = QLineEdit(self.formLayoutWidget_21)
        self.ODMRFileNumber_2.setObjectName(u"ODMRFileNumber_2")

        self.formLayout_41.setWidget(2, QFormLayout.FieldRole, self.ODMRFileNumber_2)

        self.lblComment1 = QLabel(self.formLayoutWidget_21)
        self.lblComment1.setObjectName(u"lblComment1")

        self.formLayout_41.setWidget(3, QFormLayout.LabelRole, self.lblComment1)

        self.rabiComment = QLineEdit(self.formLayoutWidget_21)
        self.rabiComment.setObjectName(u"rabiComment")

        self.formLayout_41.setWidget(4, QFormLayout.SpanningRole, self.rabiComment)

        self.btnSaveRabi = QPushButton(self.DataSave1)
        self.btnSaveRabi.setObjectName(u"btnSaveRabi")
        self.btnSaveRabi.setGeometry(QRect(230, 180, 211, 51))

        self.gridLayout1.addWidget(self.DataSave1, 2, 0, 1, 1)

        self.Rabi = QGroupBox(self.verticalWidget_21)
        self.Rabi.setObjectName(u"Rabi")
        self.Rabi.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.Rabi.sizePolicy().hasHeightForWidth())
        self.Rabi.setSizePolicy(sizePolicy2)
        self.Rabi.setMinimumSize(QSize(450, 220))
        self.Rabi.setMaximumSize(QSize(400, 16777215))
        self.Rabi.setFont(font2)
        self.gridLayout_7 = QGridLayout(self.Rabi)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.btnMeasureRabiPulse = QPushButton(self.Rabi)
        self.btnMeasureRabiPulse.setObjectName(u"btnMeasureRabiPulse")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.btnMeasureRabiPulse.sizePolicy().hasHeightForWidth())
        self.btnMeasureRabiPulse.setSizePolicy(sizePolicy5)

        self.gridLayout_7.addWidget(self.btnMeasureRabiPulse, 4, 3, 2, 1)

        self.txtWidthMW = QLineEdit(self.Rabi)
        self.txtWidthMW.setObjectName(u"txtWidthMW")

        self.gridLayout_7.addWidget(self.txtWidthMW, 2, 3, 1, 1)

        self.txtWidthImage = QLineEdit(self.Rabi)
        self.txtWidthImage.setObjectName(u"txtWidthImage")

        self.gridLayout_7.addWidget(self.txtWidthImage, 3, 3, 1, 1)

        self.lblDuration = QLabel(self.Rabi)
        self.lblDuration.setObjectName(u"lblDuration")

        self.gridLayout_7.addWidget(self.lblDuration, 0, 3, 1, 1)

        self.txtWidthPump = QLineEdit(self.Rabi)
        self.txtWidthPump.setObjectName(u"txtWidthPump")

        self.gridLayout_7.addWidget(self.txtWidthPump, 1, 3, 1, 1)

        self.txtStartReadout = QLineEdit(self.Rabi)
        self.txtStartReadout.setObjectName(u"txtStartReadout")

        self.gridLayout_7.addWidget(self.txtStartReadout, 4, 1, 1, 1)

        self.txtStartMW = QLineEdit(self.Rabi)
        self.txtStartMW.setObjectName(u"txtStartMW")

        self.gridLayout_7.addWidget(self.txtStartMW, 2, 1, 1, 1)

        self.lblImaging = QLabel(self.Rabi)
        self.lblImaging.setObjectName(u"lblImaging")

        self.gridLayout_7.addWidget(self.lblImaging, 3, 0, 1, 1)

        self.lblPump = QLabel(self.Rabi)
        self.lblPump.setObjectName(u"lblPump")

        self.gridLayout_7.addWidget(self.lblPump, 1, 0, 1, 1)

        self.lblMW = QLabel(self.Rabi)
        self.lblMW.setObjectName(u"lblMW")

        self.gridLayout_7.addWidget(self.lblMW, 2, 0, 1, 1)

        self.lblReadout = QLabel(self.Rabi)
        self.lblReadout.setObjectName(u"lblReadout")

        self.gridLayout_7.addWidget(self.lblReadout, 4, 0, 1, 1)

        self.txtStartPump = QLineEdit(self.Rabi)
        self.txtStartPump.setObjectName(u"txtStartPump")

        self.gridLayout_7.addWidget(self.txtStartPump, 1, 1, 1, 1)

        self.lblStartTime = QLabel(self.Rabi)
        self.lblStartTime.setObjectName(u"lblStartTime")

        self.gridLayout_7.addWidget(self.lblStartTime, 0, 1, 1, 2)

        self.txtStartImage = QLineEdit(self.Rabi)
        self.txtStartImage.setObjectName(u"txtStartImage")

        self.gridLayout_7.addWidget(self.txtStartImage, 3, 1, 1, 1)

        self.lblAveragesNumber = QLabel(self.Rabi)
        self.lblAveragesNumber.setObjectName(u"lblAveragesNumber")

        self.gridLayout_7.addWidget(self.lblAveragesNumber, 5, 0, 1, 1)

        self.txtAveragesNumber = QLineEdit(self.Rabi)
        self.txtAveragesNumber.setObjectName(u"txtAveragesNumber")

        self.gridLayout_7.addWidget(self.txtAveragesNumber, 5, 1, 1, 1)


        self.gridLayout1.addWidget(self.Rabi, 1, 0, 1, 1)


        self.gridLayout_21.addWidget(self.verticalWidget_21, 0, 1, 1, 1)

        self.rabiPulsePlotWidget = QWidget(self.RabiPulseTab)
        self.rabiPulsePlotWidget.setObjectName(u"rabiPulsePlotWidget")
        self.rabiPulsePlotLayout = QGridLayout(self.rabiPulsePlotWidget)
        self.rabiPulsePlotLayout.setObjectName(u"rabiPulsePlotLayout")

        self.gridLayout_21.addWidget(self.rabiPulsePlotWidget, 0, 0, 1, 1)


        self.gridLayout_41.addLayout(self.gridLayout_21, 0, 0, 1, 1)

        self.measurmentTabs.addTab(self.RabiPulseTab, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_3 = QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setSizeConstraint(QLayout.SetNoConstraint)
        self.verticalWidget_5 = QWidget(self.tab)
        self.verticalWidget_5.setObjectName(u"verticalWidget_5")
        sizePolicy3.setHeightForWidth(self.verticalWidget_5.sizePolicy().hasHeightForWidth())
        self.verticalWidget_5.setSizePolicy(sizePolicy3)
        self.gridLayout_18 = QGridLayout(self.verticalWidget_5)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.DataSave_4 = QGroupBox(self.verticalWidget_5)
        self.DataSave_4.setObjectName(u"DataSave_4")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.DataSave_4.sizePolicy().hasHeightForWidth())
        self.DataSave_4.setSizePolicy(sizePolicy6)
        self.DataSave_4.setFont(font2)
        self.gridLayout_20 = QGridLayout(self.DataSave_4)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.formLayout_10 = QFormLayout()
        self.formLayout_10.setObjectName(u"formLayout_10")
        self.formLayout_10.setSizeConstraint(QLayout.SetNoConstraint)
        self.formLayout_10.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lblPathRabi_3 = QLabel(self.DataSave_4)
        self.lblPathRabi_3.setObjectName(u"lblPathRabi_3")

        self.formLayout_10.setWidget(0, QFormLayout.LabelRole, self.lblPathRabi_3)

        self.txtPathRabi_3 = QLineEdit(self.DataSave_4)
        self.txtPathRabi_3.setObjectName(u"txtPathRabi_3")

        self.formLayout_10.setWidget(1, QFormLayout.SpanningRole, self.txtPathRabi_3)

        self.lblCommentRabi_3 = QLabel(self.DataSave_4)
        self.lblCommentRabi_3.setObjectName(u"lblCommentRabi_3")

        self.formLayout_10.setWidget(2, QFormLayout.LabelRole, self.lblCommentRabi_3)

        self.txtCommentRabi_3 = QLineEdit(self.DataSave_4)
        self.txtCommentRabi_3.setObjectName(u"txtCommentRabi_3")

        self.formLayout_10.setWidget(3, QFormLayout.SpanningRole, self.txtCommentRabi_3)


        self.gridLayout_20.addLayout(self.formLayout_10, 1, 0, 1, 1)


        self.gridLayout_18.addWidget(self.DataSave_4, 2, 0, 1, 1)

        self.widget_3 = QWidget(self.verticalWidget_5)
        self.widget_3.setObjectName(u"widget_3")

        self.gridLayout_18.addWidget(self.widget_3, 3, 0, 1, 1)

        self.Scan_2 = QGroupBox(self.verticalWidget_5)
        self.Scan_2.setObjectName(u"Scan_2")
        sizePolicy2.setHeightForWidth(self.Scan_2.sizePolicy().hasHeightForWidth())
        self.Scan_2.setSizePolicy(sizePolicy2)
        self.Scan_2.setMinimumSize(QSize(450, 160))
        self.Scan_2.setFont(font2)
        self.btnScanRabi_3 = QPushButton(self.Scan_2)
        self.btnScanRabi_3.setObjectName(u"btnScanRabi_3")
        self.btnScanRabi_3.setGeometry(QRect(230, 100, 201, 51))
        self.lblIterations_3 = QLabel(self.Scan_2)
        self.lblIterations_3.setObjectName(u"lblIterations_3")
        self.lblIterations_3.setGeometry(QRect(240, 60, 81, 16))
        self.txtIterations_3 = QLineEdit(self.Scan_2)
        self.txtIterations_3.setObjectName(u"txtIterations_3")
        self.txtIterations_3.setGeometry(QRect(330, 60, 101, 20))
        self.lblCurrentIterations = QLabel(self.Scan_2)
        self.lblCurrentIterations.setObjectName(u"lblCurrentIterations")
        self.lblCurrentIterations.setGeometry(QRect(166, 100, 61, 20))
        self.lblRange_4 = QLabel(self.Scan_2)
        self.lblRange_4.setObjectName(u"lblRange_4")
        self.lblRange_4.setGeometry(QRect(20, 30, 81, 21))
        self.txtIterations_4 = QLineEdit(self.Scan_2)
        self.txtIterations_4.setObjectName(u"txtIterations_4")
        self.txtIterations_4.setGeometry(QRect(150, 30, 81, 20))
        self.txtIterations_5 = QLineEdit(self.Scan_2)
        self.txtIterations_5.setObjectName(u"txtIterations_5")
        self.txtIterations_5.setGeometry(QRect(330, 30, 101, 20))
        self.lblRange_5 = QLabel(self.Scan_2)
        self.lblRange_5.setObjectName(u"lblRange_5")
        self.lblRange_5.setGeometry(QRect(240, 30, 81, 21))
        self.lblRange_6 = QLabel(self.Scan_2)
        self.lblRange_6.setObjectName(u"lblRange_6")
        self.lblRange_6.setGeometry(QRect(20, 60, 121, 21))
        self.txtIterations_6 = QLineEdit(self.Scan_2)
        self.txtIterations_6.setObjectName(u"txtIterations_6")
        self.txtIterations_6.setGeometry(QRect(150, 60, 81, 20))
        self.lblIterations_4 = QLabel(self.Scan_2)
        self.lblIterations_4.setObjectName(u"lblIterations_4")
        self.lblIterations_4.setGeometry(QRect(20, 100, 141, 16))

        self.gridLayout_18.addWidget(self.Scan_2, 1, 0, 1, 1)


        self.gridLayout_17.addWidget(self.verticalWidget_5, 0, 1, 1, 1)

        self.rabiScanPlotWidget = QWidget(self.tab)
        self.rabiScanPlotWidget.setObjectName(u"rabiScanPlotWidget")
        self.rabiScanPlotLayout = QGridLayout(self.rabiScanPlotWidget)
        self.rabiScanPlotLayout.setObjectName(u"rabiScanPlotLayout")

        self.gridLayout_17.addWidget(self.rabiScanPlotWidget, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_17, 0, 0, 1, 1)

        self.measurmentTabs.addTab(self.tab, "")

        self.plotLayout.addWidget(self.measurmentTabs)


        self.verticalLayout.addWidget(self.plotWidget)


        self.horizontalLayout_2.addWidget(self.verticalWidget)

        odmr.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(odmr)
        self.statusBar.setObjectName(u"statusBar")
        odmr.setStatusBar(self.statusBar)

        self.retranslateUi(odmr)

        self.measurmentTabs.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(odmr)
    # setupUi

    def retranslateUi(self, odmr):
        odmr.setWindowTitle(QCoreApplication.translate("odmr", u"ODMR & Rabi", None))
        self.PulseBlaster.setTitle(QCoreApplication.translate("odmr", u"Pulse Blaster settings", None))
        self.lblPortPulseBlaster.setText(QCoreApplication.translate("odmr", u"Port", None))
        self.btnConnectPulseBlaster.setText(QCoreApplication.translate("odmr", u"Connect", None))
        self.lblIPPulseBlaster.setText(QCoreApplication.translate("odmr", u"IP", None))
        self.RedPitaya.setTitle(QCoreApplication.translate("odmr", u"Red Pitaya settings", None))
        self.lblPortRedPitaya.setText(QCoreApplication.translate("odmr", u"Port", None))
        self.btnConnectRedPitaya.setText(QCoreApplication.translate("odmr", u"Connect", None))
        self.lblIPRedPitaya.setText(QCoreApplication.translate("odmr", u"IP", None))
        self.LaserControl.setTitle(QCoreApplication.translate("odmr", u"AOM control", None))
        self.lblLowLevel.setText(QCoreApplication.translate("odmr", u"Low [V]", None))
        self.lblHighLevel.setText(QCoreApplication.translate("odmr", u"High [V]", None))
        self.btnOpenCloseAOM.setText(QCoreApplication.translate("odmr", u"Open", None))
        self.ODMR.setTitle(QCoreApplication.translate("odmr", u"ODMR Measurement Settings", None))
        self.lblRepeatNum.setText("")
        self.lblCountDuration.setText(QCoreApplication.translate("odmr", u"Single Pulse Duration [us]", None))
        self.lblCountNumber.setText(QCoreApplication.translate("odmr", u"Number of Pulses", None))
        self.lblThreshold.setText(QCoreApplication.translate("odmr", u"Threshold [V]", None))
        self.label.setText(QCoreApplication.translate("odmr", u"Repetition?", None))
        self.label_3.setText(QCoreApplication.translate("odmr", u"Repetition Max Number", None))
        self.label_4.setText(QCoreApplication.translate("odmr", u"Current Repetetion", None))
        self.lblCurrentRepetetion.setText(QCoreApplication.translate("odmr", u"0", None))
        self.btnStartODMR.setText(QCoreApplication.translate("odmr", u"Start", None))
        self.btnStopODMR.setText(QCoreApplication.translate("odmr", u"Stop", None))
        self.MW.setTitle(QCoreApplication.translate("odmr", u"MW Generator Settings", None))
        self.lblStartFreq.setText(QCoreApplication.translate("odmr", u"Start Frequency [MHz]:", None))
        self.lblStopFreq.setText(QCoreApplication.translate("odmr", u"Stop Frequency [MHz]:", None))
        self.lblRFPower.setText(QCoreApplication.translate("odmr", u"RF Power [dBm]", None))
        self.comboBoxMWdevice.setItemText(0, QCoreApplication.translate("odmr", u"SynthHD", None))

        self.connectMicrowaveODMRButton.setText(QCoreApplication.translate("odmr", u"Connect", None))
        self.onOffODMRConnectButton.setText(QCoreApplication.translate("odmr", u"RF is Off", None))
        self.DataSave.setTitle(QCoreApplication.translate("odmr", u"Save Data", None))
        self.lblPath.setText(QCoreApplication.translate("odmr", u"Path", None))
        self.lblParamValue.setText(QCoreApplication.translate("odmr", u"Measurment Number", None))
        self.lblComment.setText(QCoreApplication.translate("odmr", u"Comment:", None))
        self.btnSaveODMR.setText(QCoreApplication.translate("odmr", u"Save", None))
        self.measurmentTabs.setTabText(self.measurmentTabs.indexOf(self.ODMRTab), QCoreApplication.translate("odmr", u"ODMR", None))
        self.MW1.setTitle(QCoreApplication.translate("odmr", u"MW Generator Settings", None))
        self.comboBoxMWdeviceRabi.setItemText(0, QCoreApplication.translate("odmr", u"SynthHD", None))

        self.connectMicrowaveRabiButton.setText(QCoreApplication.translate("odmr", u"Connect", None))
        self.onOffRabiConnectButton.setText(QCoreApplication.translate("odmr", u"RF is Off", None))
        self.lblCenterFreq.setText(QCoreApplication.translate("odmr", u"Center Freq, MHz:", None))
        self.lblRFPowerRabi.setText(QCoreApplication.translate("odmr", u"RF Power [dBm]", None))
        self.DataSave1.setTitle(QCoreApplication.translate("odmr", u"Save Data", None))
        self.lblPath1.setText(QCoreApplication.translate("odmr", u"Path", None))
        self.lblParamValue1.setText(QCoreApplication.translate("odmr", u"Measurment Number", None))
        self.lblComment1.setText(QCoreApplication.translate("odmr", u"Comment:", None))
        self.btnSaveRabi.setText(QCoreApplication.translate("odmr", u"Save", None))
        self.Rabi.setTitle(QCoreApplication.translate("odmr", u"Rabi Pulse Settings", None))
        self.btnMeasureRabiPulse.setText(QCoreApplication.translate("odmr", u"Measure", None))
        self.lblDuration.setText(QCoreApplication.translate("odmr", u"Duration, us:", None))
        self.lblImaging.setText(QCoreApplication.translate("odmr", u"Imaging pulse:", None))
        self.lblPump.setText(QCoreApplication.translate("odmr", u"Pump pulse:", None))
        self.lblMW.setText(QCoreApplication.translate("odmr", u"MW pulse:", None))
        self.lblReadout.setText(QCoreApplication.translate("odmr", u"Readout pulse:", None))
        self.lblStartTime.setText(QCoreApplication.translate("odmr", u"Start time, us:", None))
        self.lblAveragesNumber.setText(QCoreApplication.translate("odmr", u"Average Number:", None))
        self.measurmentTabs.setTabText(self.measurmentTabs.indexOf(self.RabiPulseTab), QCoreApplication.translate("odmr", u"Rabi Sequence Single Pulse", None))
        self.DataSave_4.setTitle(QCoreApplication.translate("odmr", u"Save Data", None))
        self.lblPathRabi_3.setText(QCoreApplication.translate("odmr", u"Path", None))
        self.lblCommentRabi_3.setText(QCoreApplication.translate("odmr", u"Comment:", None))
        self.Scan_2.setTitle(QCoreApplication.translate("odmr", u"Scan Control", None))
        self.btnScanRabi_3.setText(QCoreApplication.translate("odmr", u"Scan Rabi", None))
        self.lblIterations_3.setText(QCoreApplication.translate("odmr", u"Iterations", None))
        self.lblCurrentIterations.setText(QCoreApplication.translate("odmr", u"0", None))
        self.lblRange_4.setText(QCoreApplication.translate("odmr", u"Start [us]", None))
        self.lblRange_5.setText(QCoreApplication.translate("odmr", u"Stop [us]", None))
        self.lblRange_6.setText(QCoreApplication.translate("odmr", u"Time Step [us]", None))
        self.lblIterations_4.setText(QCoreApplication.translate("odmr", u"Current Iteration", None))
        self.measurmentTabs.setTabText(self.measurmentTabs.indexOf(self.tab), QCoreApplication.translate("odmr", u"Rabi Scan", None))
    # retranslateUi


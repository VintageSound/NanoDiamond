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
        odmr.resize(1312, 1130)
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
        self.ODMRPlotWidget = QWidget(self.ODMRTab)
        self.ODMRPlotWidget.setObjectName(u"ODMRPlotWidget")
        self.ODMRPlotWidget.setMinimumSize(QSize(690, 839))

        self.gridLayout_2.addWidget(self.ODMRPlotWidget, 0, 0, 1, 1)

        self.verticalWidget_2 = QWidget(self.ODMRTab)
        self.verticalWidget_2.setObjectName(u"verticalWidget_2")
        sizePolicy3.setHeightForWidth(self.verticalWidget_2.sizePolicy().hasHeightForWidth())
        self.verticalWidget_2.setSizePolicy(sizePolicy3)
        self.gridLayout = QGridLayout(self.verticalWidget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.ODMR = QGroupBox(self.verticalWidget_2)
        self.ODMR.setObjectName(u"ODMR")
        self.ODMR.setMinimumSize(QSize(450, 300))
        self.ODMR.setFont(font2)
        self.lblRepeatNum = QLabel(self.ODMR)
        self.lblRepeatNum.setObjectName(u"lblRepeatNum")
        self.lblRepeatNum.setGeometry(QRect(30, 120, 71, 16))
        self.formLayoutWidget = QWidget(self.ODMR)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 30, 431, 242))
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

        self.horizontalLayoutWidget_2 = QWidget(self.ODMR)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 240, 431, 51))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btnStartODMR = QPushButton(self.horizontalLayoutWidget_2)
        self.btnStartODMR.setObjectName(u"btnStartODMR")

        self.horizontalLayout_5.addWidget(self.btnStartODMR)

        self.btnStopODMR = QPushButton(self.horizontalLayoutWidget_2)
        self.btnStopODMR.setObjectName(u"btnStopODMR")

        self.horizontalLayout_5.addWidget(self.btnStopODMR)


        self.gridLayout.addWidget(self.ODMR, 1, 0, 1, 1)

        self.MW = QGroupBox(self.verticalWidget_2)
        self.MW.setObjectName(u"MW")
        self.MW.setEnabled(True)
        self.MW.setMinimumSize(QSize(450, 250))
        self.MW.setFont(font2)
        self.layoutWidget = QWidget(self.MW)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(18, 70, 421, 121))
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
        self.comboBoxMWdevice.setGeometry(QRect(20, 30, 99, 30))
        self.comboBoxMWdevice.setAutoFillBackground(False)
        self.comboBoxMWdevice.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.connectMicrowaveODMRButton = QPushButton(self.MW)
        self.connectMicrowaveODMRButton.setObjectName(u"connectMicrowaveODMRButton")
        self.connectMicrowaveODMRButton.setGeometry(QRect(20, 210, 121, 28))
        self.onOffODMRConnectButton = QPushButton(self.MW)
        self.onOffODMRConnectButton.setObjectName(u"onOffODMRConnectButton")
        self.onOffODMRConnectButton.setGeometry(QRect(160, 210, 111, 28))
        self.applyMicrowaveODMRButton = QPushButton(self.MW)
        self.applyMicrowaveODMRButton.setObjectName(u"applyMicrowaveODMRButton")
        self.applyMicrowaveODMRButton.setGeometry(QRect(300, 210, 121, 28))

        self.gridLayout.addWidget(self.MW, 0, 0, 1, 1)

        self.DataSave = QGroupBox(self.verticalWidget_2)
        self.DataSave.setObjectName(u"DataSave")
        self.DataSave.setFont(font2)
        self.formLayoutWidget_2 = QWidget(self.DataSave)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(9, 22, 431, 171))
        self.formLayout_4 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lblPath = QLabel(self.formLayoutWidget_2)
        self.lblPath.setObjectName(u"lblPath")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.lblPath)

        self.lblParamValue = QLabel(self.formLayoutWidget_2)
        self.lblParamValue.setObjectName(u"lblParamValue")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.lblParamValue)

        self.txtNum = QLineEdit(self.formLayoutWidget_2)
        self.txtNum.setObjectName(u"txtNum")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.txtNum)

        self.lblComment = QLabel(self.formLayoutWidget_2)
        self.lblComment.setObjectName(u"lblComment")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.lblComment)

        self.txtPath = QLineEdit(self.formLayoutWidget_2)
        self.txtPath.setObjectName(u"txtPath")

        self.formLayout_4.setWidget(1, QFormLayout.SpanningRole, self.txtPath)

        self.txtComment = QLineEdit(self.formLayoutWidget_2)
        self.txtComment.setObjectName(u"txtComment")

        self.formLayout_4.setWidget(4, QFormLayout.SpanningRole, self.txtComment)

        self.btnSaveODMR = QPushButton(self.DataSave)
        self.btnSaveODMR.setObjectName(u"btnSaveODMR")
        self.btnSaveODMR.setGeometry(QRect(10, 210, 421, 33))

        self.gridLayout.addWidget(self.DataSave, 2, 0, 1, 1)


        self.gridLayout_2.addWidget(self.verticalWidget_2, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.measurmentTabs.addTab(self.ODMRTab, "")
        self.RabiPulseTab = QWidget()
        self.RabiPulseTab.setObjectName(u"RabiPulseTab")
        self.gridLayout_11 = QGridLayout(self.RabiPulseTab)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setSizeConstraint(QLayout.SetNoConstraint)
        self.ODMRPlotwidget_2 = QWidget(self.RabiPulseTab)
        self.ODMRPlotwidget_2.setObjectName(u"ODMRPlotwidget_2")
        self.ODMRPlotwidget_2.setMinimumSize(QSize(690, 839))

        self.gridLayout_9.addWidget(self.ODMRPlotwidget_2, 0, 0, 1, 1)

        self.verticalWidget_3 = QWidget(self.RabiPulseTab)
        self.verticalWidget_3.setObjectName(u"verticalWidget_3")
        sizePolicy3.setHeightForWidth(self.verticalWidget_3.sizePolicy().hasHeightForWidth())
        self.verticalWidget_3.setSizePolicy(sizePolicy3)
        self.gridLayout_10 = QGridLayout(self.verticalWidget_3)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.MW_3 = QGroupBox(self.verticalWidget_3)
        self.MW_3.setObjectName(u"MW_3")
        self.MW_3.setEnabled(True)
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.MW_3.sizePolicy().hasHeightForWidth())
        self.MW_3.setSizePolicy(sizePolicy5)
        self.MW_3.setMinimumSize(QSize(450, 250))
        self.MW_3.setFont(font2)
        self.gridLayout_6 = QGridLayout(self.MW_3)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.comboBoxMWdevice_3 = QComboBox(self.MW_3)
        self.comboBoxMWdevice_3.addItem("")
        self.comboBoxMWdevice_3.setObjectName(u"comboBoxMWdevice_3")
        self.comboBoxMWdevice_3.setAutoFillBackground(False)
        self.comboBoxMWdevice_3.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.gridLayout_6.addWidget(self.comboBoxMWdevice_3, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.connectMicrowaveRabiButton = QPushButton(self.MW_3)
        self.connectMicrowaveRabiButton.setObjectName(u"connectMicrowaveRabiButton")

        self.horizontalLayout_3.addWidget(self.connectMicrowaveRabiButton)

        self.onOffRabiConnectButton = QPushButton(self.MW_3)
        self.onOffRabiConnectButton.setObjectName(u"onOffRabiConnectButton")
        self.onOffRabiConnectButton.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.onOffRabiConnectButton)

        self.applyMicrowaveRabiButton = QPushButton(self.MW_3)
        self.applyMicrowaveRabiButton.setObjectName(u"applyMicrowaveRabiButton")

        self.horizontalLayout_3.addWidget(self.applyMicrowaveRabiButton)


        self.gridLayout_6.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.lblRFPower_3 = QLabel(self.MW_3)
        self.lblRFPower_3.setObjectName(u"lblRFPower_3")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.lblRFPower_3)

        self.txtRFPowerRabi = QLineEdit(self.MW_3)
        self.txtRFPowerRabi.setObjectName(u"txtRFPowerRabi")

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.txtRFPowerRabi)

        self.lblCenterFreq_2 = QLabel(self.MW_3)
        self.lblCenterFreq_2.setObjectName(u"lblCenterFreq_2")

        self.formLayout_5.setWidget(0, QFormLayout.LabelRole, self.lblCenterFreq_2)

        self.txtCenterFreq = QLineEdit(self.MW_3)
        self.txtCenterFreq.setObjectName(u"txtCenterFreq")

        self.formLayout_5.setWidget(0, QFormLayout.FieldRole, self.txtCenterFreq)


        self.gridLayout_6.addLayout(self.formLayout_5, 1, 0, 1, 1)


        self.gridLayout_10.addWidget(self.MW_3, 0, 0, 1, 1)

        self.DataSave_2 = QGroupBox(self.verticalWidget_3)
        self.DataSave_2.setObjectName(u"DataSave_2")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.DataSave_2.sizePolicy().hasHeightForWidth())
        self.DataSave_2.setSizePolicy(sizePolicy6)
        self.DataSave_2.setFont(font2)
        self.gridLayout_8 = QGridLayout(self.DataSave_2)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.formLayout_6.setSizeConstraint(QLayout.SetNoConstraint)
        self.formLayout_6.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lblPathRabi = QLabel(self.DataSave_2)
        self.lblPathRabi.setObjectName(u"lblPathRabi")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.lblPathRabi)

        self.lblParamValue_2 = QLabel(self.DataSave_2)
        self.lblParamValue_2.setObjectName(u"lblParamValue_2")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.lblParamValue_2)

        self.txtIndexRai = QLineEdit(self.DataSave_2)
        self.txtIndexRai.setObjectName(u"txtIndexRai")

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.txtIndexRai)

        self.lblCommentRabi = QLabel(self.DataSave_2)
        self.lblCommentRabi.setObjectName(u"lblCommentRabi")

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.lblCommentRabi)

        self.txtPathRabi = QLineEdit(self.DataSave_2)
        self.txtPathRabi.setObjectName(u"txtPathRabi")

        self.formLayout_6.setWidget(1, QFormLayout.SpanningRole, self.txtPathRabi)

        self.btnSaveRabi = QPushButton(self.DataSave_2)
        self.btnSaveRabi.setObjectName(u"btnSaveRabi")

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.btnSaveRabi)

        self.txtCommentRabi = QLineEdit(self.DataSave_2)
        self.txtCommentRabi.setObjectName(u"txtCommentRabi")

        self.formLayout_6.setWidget(4, QFormLayout.SpanningRole, self.txtCommentRabi)


        self.gridLayout_8.addLayout(self.formLayout_6, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.DataSave_2, 2, 0, 1, 1)

        self.Rabi = QGroupBox(self.verticalWidget_3)
        self.Rabi.setObjectName(u"Rabi")
        self.Rabi.setEnabled(True)
        sizePolicy2.setHeightForWidth(self.Rabi.sizePolicy().hasHeightForWidth())
        self.Rabi.setSizePolicy(sizePolicy2)
        self.Rabi.setMinimumSize(QSize(450, 220))
        self.Rabi.setMaximumSize(QSize(400, 16777215))
        self.Rabi.setFont(font2)
        self.gridLayout_7 = QGridLayout(self.Rabi)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.txtStartReadout = QLineEdit(self.Rabi)
        self.txtStartReadout.setObjectName(u"txtStartReadout")

        self.gridLayout_7.addWidget(self.txtStartReadout, 4, 1, 1, 1)

        self.lblDuration = QLabel(self.Rabi)
        self.lblDuration.setObjectName(u"lblDuration")

        self.gridLayout_7.addWidget(self.lblDuration, 0, 3, 1, 1)

        self.txtWidthPump = QLineEdit(self.Rabi)
        self.txtWidthPump.setObjectName(u"txtWidthPump")

        self.gridLayout_7.addWidget(self.txtWidthPump, 1, 3, 1, 1)

        self.txtWidthMW = QLineEdit(self.Rabi)
        self.txtWidthMW.setObjectName(u"txtWidthMW")

        self.gridLayout_7.addWidget(self.txtWidthMW, 2, 3, 1, 1)

        self.txtWidthImage = QLineEdit(self.Rabi)
        self.txtWidthImage.setObjectName(u"txtWidthImage")

        self.gridLayout_7.addWidget(self.txtWidthImage, 3, 3, 1, 1)

        self.txtAveragesNumber = QLineEdit(self.Rabi)
        self.txtAveragesNumber.setObjectName(u"txtAveragesNumber")

        self.gridLayout_7.addWidget(self.txtAveragesNumber, 5, 1, 1, 1)

        self.lblMW = QLabel(self.Rabi)
        self.lblMW.setObjectName(u"lblMW")

        self.gridLayout_7.addWidget(self.lblMW, 2, 0, 1, 1)

        self.txtStartMW = QLineEdit(self.Rabi)
        self.txtStartMW.setObjectName(u"txtStartMW")

        self.gridLayout_7.addWidget(self.txtStartMW, 2, 1, 1, 1)

        self.lblPump = QLabel(self.Rabi)
        self.lblPump.setObjectName(u"lblPump")

        self.gridLayout_7.addWidget(self.lblPump, 1, 0, 1, 1)

        self.lblImaging = QLabel(self.Rabi)
        self.lblImaging.setObjectName(u"lblImaging")

        self.gridLayout_7.addWidget(self.lblImaging, 3, 0, 1, 1)

        self.txtStartImage = QLineEdit(self.Rabi)
        self.txtStartImage.setObjectName(u"txtStartImage")

        self.gridLayout_7.addWidget(self.txtStartImage, 3, 1, 1, 1)

        self.txtStartPump = QLineEdit(self.Rabi)
        self.txtStartPump.setObjectName(u"txtStartPump")

        self.gridLayout_7.addWidget(self.txtStartPump, 1, 1, 1, 1)

        self.lblAveragesNumber = QLabel(self.Rabi)
        self.lblAveragesNumber.setObjectName(u"lblAveragesNumber")

        self.gridLayout_7.addWidget(self.lblAveragesNumber, 5, 0, 1, 1)

        self.lblStartTime = QLabel(self.Rabi)
        self.lblStartTime.setObjectName(u"lblStartTime")

        self.gridLayout_7.addWidget(self.lblStartTime, 0, 1, 1, 2)

        self.lblReadout = QLabel(self.Rabi)
        self.lblReadout.setObjectName(u"lblReadout")

        self.gridLayout_7.addWidget(self.lblReadout, 4, 0, 1, 1)

        self.btnMeasureRabiPulse = QPushButton(self.Rabi)
        self.btnMeasureRabiPulse.setObjectName(u"btnMeasureRabiPulse")

        self.gridLayout_7.addWidget(self.btnMeasureRabiPulse, 4, 3, 3, 1)


        self.gridLayout_10.addWidget(self.Rabi, 1, 0, 1, 1)

        self.widget = QWidget(self.verticalWidget_3)
        self.widget.setObjectName(u"widget")

        self.gridLayout_10.addWidget(self.widget, 3, 0, 1, 1)


        self.gridLayout_9.addWidget(self.verticalWidget_3, 0, 1, 1, 1)


        self.gridLayout_11.addLayout(self.gridLayout_9, 0, 0, 1, 1)

        self.measurmentTabs.addTab(self.RabiPulseTab, "")
        self.FullRabiTab = QWidget()
        self.FullRabiTab.setObjectName(u"FullRabiTab")
        self.Scan_2 = QGroupBox(self.FullRabiTab)
        self.Scan_2.setObjectName(u"Scan_2")
        self.Scan_2.setGeometry(QRect(220, 100, 450, 130))
        sizePolicy1.setHeightForWidth(self.Scan_2.sizePolicy().hasHeightForWidth())
        self.Scan_2.setSizePolicy(sizePolicy1)
        self.Scan_2.setMinimumSize(QSize(0, 130))
        self.Scan_2.setFont(font2)
        self.label_2 = QLabel(self.Scan_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 30, 141, 21))
        self.cmbScanParam_2 = QComboBox(self.Scan_2)
        self.cmbScanParam_2.setObjectName(u"cmbScanParam_2")
        self.cmbScanParam_2.setGeometry(QRect(170, 30, 111, 22))
        self.lblRange_2 = QLabel(self.Scan_2)
        self.lblRange_2.setObjectName(u"lblRange_2")
        self.lblRange_2.setGeometry(QRect(100, 60, 61, 21))
        self.txtRange_2 = QLineEdit(self.Scan_2)
        self.txtRange_2.setObjectName(u"txtRange_2")
        self.txtRange_2.setGeometry(QRect(170, 60, 111, 20))
        self.btnScanRabi_2 = QPushButton(self.Scan_2)
        self.btnScanRabi_2.setObjectName(u"btnScanRabi_2")
        self.btnScanRabi_2.setGeometry(QRect(320, 30, 101, 51))
        self.lblCurrentValue_2 = QLabel(self.Scan_2)
        self.lblCurrentValue_2.setObjectName(u"lblCurrentValue_2")
        self.lblCurrentValue_2.setGeometry(QRect(30, 60, 61, 21))
        self.lblIterations_2 = QLabel(self.Scan_2)
        self.lblIterations_2.setObjectName(u"lblIterations_2")
        self.lblIterations_2.setGeometry(QRect(80, 90, 81, 16))
        self.txtIterations_2 = QLineEdit(self.Scan_2)
        self.txtIterations_2.setObjectName(u"txtIterations_2")
        self.txtIterations_2.setGeometry(QRect(170, 90, 113, 20))
        self.lblCurrentIterations_2 = QLabel(self.Scan_2)
        self.lblCurrentIterations_2.setObjectName(u"lblCurrentIterations_2")
        self.lblCurrentIterations_2.setGeometry(QRect(30, 90, 47, 16))
        self.measurmentTabs.addTab(self.FullRabiTab, "")

        self.plotLayout.addWidget(self.measurmentTabs)


        self.verticalLayout.addWidget(self.plotWidget)


        self.horizontalLayout_2.addWidget(self.verticalWidget)

        odmr.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(odmr)
        self.statusBar.setObjectName(u"statusBar")
        odmr.setStatusBar(self.statusBar)

        self.retranslateUi(odmr)

        self.measurmentTabs.setCurrentIndex(0)


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
        self.applyMicrowaveODMRButton.setText(QCoreApplication.translate("odmr", u"Apply", None))
        self.DataSave.setTitle(QCoreApplication.translate("odmr", u"Save Data", None))
        self.lblPath.setText(QCoreApplication.translate("odmr", u"Path", None))
        self.lblParamValue.setText(QCoreApplication.translate("odmr", u"Measurment Number", None))
        self.lblComment.setText(QCoreApplication.translate("odmr", u"Comment:", None))
        self.btnSaveODMR.setText(QCoreApplication.translate("odmr", u"Save", None))
        self.measurmentTabs.setTabText(self.measurmentTabs.indexOf(self.ODMRTab), QCoreApplication.translate("odmr", u"ODMR", None))
        self.MW_3.setTitle(QCoreApplication.translate("odmr", u"MW Generator Settings", None))
        self.comboBoxMWdevice_3.setItemText(0, QCoreApplication.translate("odmr", u"SynthHD", None))

        self.connectMicrowaveRabiButton.setText(QCoreApplication.translate("odmr", u"Connect", None))
        self.onOffRabiConnectButton.setText(QCoreApplication.translate("odmr", u"RF is Off", None))
        self.applyMicrowaveRabiButton.setText(QCoreApplication.translate("odmr", u"Apply", None))
        self.lblRFPower_3.setText(QCoreApplication.translate("odmr", u"RF Power [dBm]", None))
        self.lblCenterFreq_2.setText(QCoreApplication.translate("odmr", u"Center Freq, MHz:", None))
        self.DataSave_2.setTitle(QCoreApplication.translate("odmr", u"Save Data", None))
        self.lblPathRabi.setText(QCoreApplication.translate("odmr", u"Path", None))
        self.lblParamValue_2.setText(QCoreApplication.translate("odmr", u"Measurment Index", None))
        self.lblCommentRabi.setText(QCoreApplication.translate("odmr", u"Comment:", None))
        self.btnSaveRabi.setText(QCoreApplication.translate("odmr", u"Save", None))
        self.Rabi.setTitle(QCoreApplication.translate("odmr", u"Rabi Pulse Settings", None))
        self.lblDuration.setText(QCoreApplication.translate("odmr", u"Duration, us:", None))
        self.lblMW.setText(QCoreApplication.translate("odmr", u"MW pulse:", None))
        self.lblPump.setText(QCoreApplication.translate("odmr", u"Pump pulse:", None))
        self.lblImaging.setText(QCoreApplication.translate("odmr", u"Imaging pulse:", None))
        self.lblAveragesNumber.setText(QCoreApplication.translate("odmr", u"Averages number:", None))
        self.lblStartTime.setText(QCoreApplication.translate("odmr", u"Start time, us:", None))
        self.lblReadout.setText(QCoreApplication.translate("odmr", u"Readout pulse:", None))
        self.btnMeasureRabiPulse.setText(QCoreApplication.translate("odmr", u"Measure", None))
        self.measurmentTabs.setTabText(self.measurmentTabs.indexOf(self.RabiPulseTab), QCoreApplication.translate("odmr", u"Rabi Pulse Sequence", None))
        self.Scan_2.setTitle(QCoreApplication.translate("odmr", u"Scan Control", None))
        self.label_2.setText(QCoreApplication.translate("odmr", u"Scan parameter:", None))
        self.lblRange_2.setText(QCoreApplication.translate("odmr", u"Range:", None))
        self.txtRange_2.setPlaceholderText(QCoreApplication.translate("odmr", u"start,stop,step_size", None))
        self.btnScanRabi_2.setText(QCoreApplication.translate("odmr", u"Scan Rabi", None))
        self.lblCurrentValue_2.setText("")
        self.lblIterations_2.setText(QCoreApplication.translate("odmr", u"Iterations:", None))
        self.lblCurrentIterations_2.setText("")
        self.measurmentTabs.setTabText(self.measurmentTabs.indexOf(self.FullRabiTab), QCoreApplication.translate("odmr", u"Full Rabi", None))
    # retranslateUi


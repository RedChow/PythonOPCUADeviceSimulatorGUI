# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableView, QVBoxLayout,
    QWidget)

from device_tree import DeviceTree

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionTimer_and_Device_Editor = QAction(MainWindow)
        self.actionTimer_and_Device_Editor.setObjectName(u"actionTimer_and_Device_Editor")
        self.actionAdd_Directory = QAction(MainWindow)
        self.actionAdd_Directory.setObjectName(u"actionAdd_Directory")
        self.actionAdd_File = QAction(MainWindow)
        self.actionAdd_File.setObjectName(u"actionAdd_File")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.devicesTreeView = DeviceTree(self.dockWidgetContents)
        self.devicesTreeView.setObjectName(u"devicesTreeView")

        self.verticalLayout.addWidget(self.devicesTreeView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pushButtonAddDevice = QPushButton(self.dockWidgetContents)
        self.pushButtonAddDevice.setObjectName(u"pushButtonAddDevice")

        self.horizontalLayout_3.addWidget(self.pushButtonAddDevice)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget_2 = QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName(u"dockWidget_2")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.horizontalLayout_2 = QHBoxLayout(self.dockWidgetContents_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.dockWidgetContents_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.lineEditOPCUAServerAddress = QLineEdit(self.dockWidgetContents_2)
        self.lineEditOPCUAServerAddress.setObjectName(u"lineEditOPCUAServerAddress")

        self.horizontalLayout.addWidget(self.lineEditOPCUAServerAddress)

        self.pushButtonStartOPCUAServer = QPushButton(self.dockWidgetContents_2)
        self.pushButtonStartOPCUAServer.setObjectName(u"pushButtonStartOPCUAServer")

        self.horizontalLayout.addWidget(self.pushButtonStartOPCUAServer)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.dockWidgetContents_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.labelIsOPCUAServerRunning = QLabel(self.dockWidgetContents_2)
        self.labelIsOPCUAServerRunning.setObjectName(u"labelIsOPCUAServerRunning")

        self.horizontalLayout.addWidget(self.labelIsOPCUAServerRunning)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.dockWidget_2)
        self.dockWidget_3 = QDockWidget(MainWindow)
        self.dockWidget_3.setObjectName(u"dockWidget_3")
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.verticalLayout_4 = QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tableView = QTableView(self.dockWidgetContents_3)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_4.addWidget(self.tableView)

        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_3)
        self.dockWidget_4 = QDockWidget(MainWindow)
        self.dockWidget_4.setObjectName(u"dockWidget_4")
        self.dockWidgetContents_4 = QWidget()
        self.dockWidgetContents_4.setObjectName(u"dockWidgetContents_4")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.dockWidgetContents_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFrameShape(QFrame.Box)

        self.verticalLayout_3.addWidget(self.label_4)

        self.dockWidget_4.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(Qt.RightDockWidgetArea, self.dockWidget_4)
        self.dockWidget_5 = QDockWidget(MainWindow)
        self.dockWidget_5.setObjectName(u"dockWidget_5")
        self.dockWidgetContents_5 = QWidget()
        self.dockWidgetContents_5.setObjectName(u"dockWidgetContents_5")
        self.verticalLayout_5 = QVBoxLayout(self.dockWidgetContents_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tableViewTimers = QTableView(self.dockWidgetContents_5)
        self.tableViewTimers.setObjectName(u"tableViewTimers")

        self.verticalLayout_5.addWidget(self.tableViewTimers)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.dockWidget_5.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget_5)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionTimer_and_Device_Editor)
        self.menuFile.addAction(self.actionAdd_Directory)
        self.menuFile.addAction(self.actionAdd_File)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionTimer_and_Device_Editor.setText(QCoreApplication.translate("MainWindow", u"Timer and Device Editor", None))
        self.actionAdd_Directory.setText(QCoreApplication.translate("MainWindow", u"Add Directory", None))
        self.actionAdd_File.setText(QCoreApplication.translate("MainWindow", u"Add File", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.pushButtonAddDevice.setText(QCoreApplication.translate("MainWindow", u"Add New Device", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Server Address:", None))
        self.lineEditOPCUAServerAddress.setText(QCoreApplication.translate("MainWindow", u"opc.tcp://0.0.0.0:4840", None))
        self.pushButtonStartOPCUAServer.setText(QCoreApplication.translate("MainWindow", u"Start Server", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Server Status", None))
        self.labelIsOPCUAServerRunning.setText(QCoreApplication.translate("MainWindow", u"Not Running", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi


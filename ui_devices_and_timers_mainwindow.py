# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'devices_and_timers_mainwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTableView, QVBoxLayout, QWidget)

class Ui_DevicesAndTimersMainWindow(object):
    def setupUi(self, DevicesAndTimersMainWindow):
        if not DevicesAndTimersMainWindow.objectName():
            DevicesAndTimersMainWindow.setObjectName(u"DevicesAndTimersMainWindow")
        DevicesAndTimersMainWindow.resize(800, 600)
        self.actionSave_to_File = QAction(DevicesAndTimersMainWindow)
        self.actionSave_to_File.setObjectName(u"actionSave_to_File")
        self.actionOpen_File = QAction(DevicesAndTimersMainWindow)
        self.actionOpen_File.setObjectName(u"actionOpen_File")
        self.centralwidget = QWidget(DevicesAndTimersMainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tableViewTimers = QTableView(self.widget)
        self.tableViewTimers.setObjectName(u"tableViewTimers")

        self.verticalLayout.addWidget(self.tableViewTimers)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_2 = QSpacerItem(128, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.pushButtonAddTimer = QPushButton(self.widget)
        self.pushButtonAddTimer.setObjectName(u"pushButtonAddTimer")

        self.horizontalLayout_4.addWidget(self.pushButtonAddTimer)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.splitter.addWidget(self.widget)
        self.widget1 = QWidget(self.splitter)
        self.widget1.setObjectName(u"widget1")
        self.verticalLayout_2 = QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.widget1)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.tableViewDevices = QTableView(self.widget1)
        self.tableViewDevices.setObjectName(u"tableViewDevices")

        self.verticalLayout_2.addWidget(self.tableViewDevices)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pushButtonAddVariable = QPushButton(self.widget1)
        self.pushButtonAddVariable.setObjectName(u"pushButtonAddVariable")

        self.horizontalLayout_2.addWidget(self.pushButtonAddVariable)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.splitter.addWidget(self.widget1)

        self.verticalLayout_3.addWidget(self.splitter)

        DevicesAndTimersMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(DevicesAndTimersMainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        DevicesAndTimersMainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(DevicesAndTimersMainWindow)
        self.statusbar.setObjectName(u"statusbar")
        DevicesAndTimersMainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen_File)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_to_File)

        self.retranslateUi(DevicesAndTimersMainWindow)

        QMetaObject.connectSlotsByName(DevicesAndTimersMainWindow)
    # setupUi

    def retranslateUi(self, DevicesAndTimersMainWindow):
        DevicesAndTimersMainWindow.setWindowTitle(QCoreApplication.translate("DevicesAndTimersMainWindow", u"MainWindow", None))
        self.actionSave_to_File.setText(QCoreApplication.translate("DevicesAndTimersMainWindow", u"Save to File", None))
        self.actionOpen_File.setText(QCoreApplication.translate("DevicesAndTimersMainWindow", u"Open File", None))
        self.label.setText(QCoreApplication.translate("DevicesAndTimersMainWindow", u"Timers", None))
        self.pushButtonAddTimer.setText(QCoreApplication.translate("DevicesAndTimersMainWindow", u"Add Timer", None))
        self.label_2.setText(QCoreApplication.translate("DevicesAndTimersMainWindow", u"Variables", None))
        self.pushButtonAddVariable.setText(QCoreApplication.translate("DevicesAndTimersMainWindow", u"Add Variable", None))
        self.menuFile.setTitle(QCoreApplication.translate("DevicesAndTimersMainWindow", u"File", None))
    # retranslateUi


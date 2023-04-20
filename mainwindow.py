# This Python file uses the following encoding: utf-8
import sys
import threading
from opcua_server import OPCUAServer
import xml_parsing_library
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Slot, QModelIndex
import functools
# Important:
# You need to run the following command to generate the ui_form.py file
# pyside6-uic main_window.ui -o ui_main_window.py
from ui_main_window import Ui_MainWindow
import devices_and_timer_editor
from logging import config
import logging
import time
import lxml

config.fileConfig("log_conf.conf")
logger = logging.getLogger('main')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("OPC-UA Devices Simulator")

        self.opcua_server = OPCUAServer()
        self.ui.pushButtonStartOPCUAServer.pressed.connect(self.start_opcua_server)
        self.opcua_server.start_server_feedback.connect(self.opc_server_feedback)
        self.timers = []

        self.ui.actionTimer_and_Device_Editor.triggered.connect(self.open_device_and_timers_editor)
        self.devices_and_timer_editor = None

        self.ui.actionAdd_Directory.triggered.connect(self.populate_treeview_directory)
        self.ui.actionAdd_File.triggered.connect(self.populate_treeview_file)
        # self.ui.pushButtonAddDevice.clicked.connect(self.ui.devicesTreeView.add_device)
        self.ui.pushButtonAddDevice.clicked.connect(self.open_device_and_timers_editor)

    def opc_server_feedback(self):
        if self.opcua_server.server_started:
            self.ui.labelIsOPCUAServerRunning.setText('Running')
        else:
            self.ui.labelIsOPCUAServerRunning.setText('Not Running')

    def open_device_and_timers_editor(self):
        self.devices_and_timer_editor = devices_and_timer_editor.MainWindow()
        self.devices_and_timer_editor.add_device.connect(self.add_device)
        self.devices_and_timer_editor.show()

    @Slot(lxml.etree._ElementTree)
    def add_device(self, data):
        """
        TODO : This is repeated code from another function below. Need to refactor
        TODO : Done, but need testing before removing this note
        :param data:
        :return:
        """
        fsp = xml_parsing_library.XMLParser(self.opcua_server)
        fsp.parse_xml('', data)
        self.add_parsed_data(fsp)

    def add_parsed_data(self, fsp):
        for t in fsp.opcua_paths_and_nodes:
            self.ui.devicesTreeView.add_data(t)
        removal_timers = []
        for timer in self.timers:
            if len(timer.functions) == 0:
                removal_timers.append(timer)
        for timer in removal_timers:
            self.timers.remove(timer)
        for timer in fsp.timer_instances:
            if timer not in self.timers:
                self.timers.append(timer)
        self.start_timers()

    def start_timers(self):
        for i, t in enumerate(self.timers):
            callback = functools.partial(self.timer_factory, index=i)
            t.timeout.connect(callback)
            t.setInterval(t.interval_milliseconds)
            t.start()

    @Slot(int)
    def timer_factory(self, index):
        t = self.timers[index]
        t.evaluate_functions()
        if t.is_random:
            new_start = t.set_random_timeout()
            t.start(new_start)
        self.ui.devicesTreeView.model().update_data()

    def start_opcua_server(self):
        server_address = self.ui.lineEditOPCUAServerAddress.text()
        if not server_address:
            return
        self.opcua_server.set_address(server_address)
        server_thread = threading.Thread(target=self.opcua_server.start_server, daemon=True)
        try:
            server_thread.start()
        except Exception as e:
            logger.error(f"Could not start OPC-UA server. Error info: {e}")

    def populate_treeview_directory(self):
        if not self.opcua_server.server_started:
            message_box = QMessageBox(self)
            message_box.setText("Server has not been started. Start server before adding variables.")
            message_box.show()
            return
        file_name = QFileDialog.getExistingDirectory(self, "Open Directory", ".",
                                                     QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if file_name:
            self.populate_variable_treeview(file_name, True)

    def populate_treeview_file(self):
        if not self.opcua_server.server_started:
            message_box = QMessageBox(self)
            message_box.setText("Server has not been started. Start server before adding variables.")
            message_box.show()
            return
        file_names = QFileDialog.getOpenFileNames(self, "Open File(s)", ".", "XML Files (*.xml)")
        if file_names:
            for file_name in file_names[0]:
                self.populate_variable_treeview(file_name, False)

    def populate_variable_treeview(self, url, is_directory):
        # TODO: Make this a function that accepts paths and nodes instead of url; parse file/directory in appropriate
        # TODO: functions above.
        # TODO: Done, but need testing before removing this note
        fsp = xml_parsing_library.XMLParser(self.opcua_server)
        if is_directory:
            fsp.parse_directory(url)
        else:
            fsp.parse_file(url)
        self.add_parsed_data(fsp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

import device_and_timers_model
import sys
import xml_parsing_library
from ui_devices_and_timers_mainwindow import Ui_DevicesAndTimersMainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import Signal
import lxml


class MainWindow(QMainWindow):
    add_device = Signal(lxml.etree._ElementTree)

    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_DevicesAndTimersMainWindow()
        self.ui.setupUi(self)
        self.timers_model = None
        self.device_model = None
        self.timer_names = []
        self.ui.actionSave_to_File.triggered.connect(self.save_to_file)
        self.ui.actionOpen_File.triggered.connect(self.load_data)
        self.ui.pushButtonAddVariable.pressed.connect(self.add_variable)
        self.ui.pushButtonAddTimer.pressed.connect(self.add_timer)
        self.ui.pushButtonAddToDeviceTree.pressed.connect(self.add_device_to_main_window)

    def add_device_to_main_window(self):
        xml_writer = xml_parsing_library.XMLCreator('')
        timer_data, device_data = self.return_timer_and_device_xml()
        xml_doc = xml_writer.create_xml_document(timer_data, device_data)
        self.add_device.emit(xml_doc)
        self.close()

    def add_timer(self):
        if self.timers_model is None:
            self.create_timers_model([])
        if self.timers_model is not None:
            self.timers_model.add_timer()
            self.ui.tableViewTimers.model().layoutChanged.emit()

    def add_variable(self):
        if self.device_model is None:
            self.create_devices_model([])
        if self.device_model is not None:
            self.device_model.add_device()
            self.ui.tableViewDevices.model().layoutChanged.emit()

    def save_to_file(self):
        file_name_parts = QFileDialog.getSaveFileName(self, "Save As", ".", "XML Files (*.xml)")
        if not file_name_parts[0]:
            return
        file_name = file_name_parts[0]
        if not file_name.endswith('.xml'):
            file_name = file_name_parts[0] + '.xml'
        xml_writer = xml_parsing_library.XMLCreator(file_name)
        timer_data, device_data = self.return_timer_and_device_xml()
        message = "There was an error writing the document. Please check the logs for more information."
        if xml_writer.write_data_to_file(timer_data, device_data):
            message = "Document was successfully written."
        message_box = QMessageBox()
        message_box.setText(message)
        message_box.exec()

    def return_timer_and_device_xml(self):
        timer_data = []
        for timer in self.timers_model.timer_data:
            if not timer[0] and not timer[1]:
                continue
            timer_dict = {'name': timer[0], 'type': timer[1]}
            if timer_dict['type'] == 'random':
                timer_dict['min'] = timer[2]
                timer_dict['max'] = timer[3]
            elif timer_dict['type'] == 'periodic':
                timer_dict['timeout'] = timer[4]
            timer_data.append(timer_dict)

        device_data = []
        device = {}
        for row in self.device_model.devices_data:
            if not all(row[0:-1]):
                continue
            path_parts = row[0].split('/')
            device_name = path_parts[0]
            not_found = True
            for i, d in enumerate(device_data):
                if d['name'] == device_name:
                    not_found = False
                    break
            if not_found:
                device['name'] = device_name
                device['variables'] = []
                device_data.append(device)
            else:
                device = device_data[i]
            device['variables'].append({'path': row[0].replace(device_name + '/', '') + '/' + row[1],
                                        'function': row[4], 'datatype': row[2].name.lower(), 'timer': row[3], 'func_arg_1': row[5],
                                        'func_arg_2': row[6], 'func_arg_3': row[7], 'func_arg_4': row[8],
                                        'func_arg_5': row[9]})
        return timer_data, device_data

    def load_data(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File", ".", "XML (*.xml)")[0]
        if not file_name:
            return
        xpl = xml_parsing_library.XMLParser(None)
        xpl.parse_file(file_name)
        self.timer_names = [x[0] for x in xpl.timer_model_data]
        self.create_devices_model(xpl.device_model_data)
        self.create_timers_model(xpl.timer_model_data)

    def create_devices_model(self, model_data):
        self.device_model = device_and_timers_model.DevicesModel(model_data)
        self.ui.tableViewDevices.setModel(self.device_model)
        self.ui.tableViewDevices.setItemDelegate(device_and_timers_model.DeviceDelegate(self))
        self.ui.tableViewDevices.horizontalHeader().setStretchLastSection(True)
        self.ui.tableViewDevices.resizeColumnsToContents()

    def create_timers_model(self, model_data):
        self.timers_model = device_and_timers_model.TimersModel(model_data)
        self.ui.tableViewTimers.setModel(self.timers_model)
        self.ui.tableViewTimers.setItemDelegate(device_and_timers_model.TimerDelegate(self))
        self.timers_model.timer_changed.connect(self.timer_name_changed)
        self.ui.tableViewTimers.horizontalHeader().setStretchLastSection(True)
        self.ui.tableViewTimers.resizeColumnsToContents()

    def timer_name_changed(self, row):
        if row >= len(self.timer_names):
            self.timer_names.append(self.timers_model.timer_data[row][0])
        else:
            self.timer_names[row] = self.timers_model.timer_data[row][0]


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

import opcua
from PySide6 import QtCore, QtWidgets, Qt
from PySide6.QtGui import QContextMenuEvent, QAction
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QInputDialog, QLineEdit
import qtree_node_model
from opcua_server import OPCUAServer, OPCDevice
import data_types


class DeviceTree(QtWidgets.QTreeView):
    remove_function = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(qtree_node_model.OPCUAInfoModel([]))
        self.setWindowTitle("test")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        context = QtWidgets.QMenu(self)
        # TODO: Implement the following context menu events. It will take a significant amount of work, but possible.
        # TODO: Might be better to use window for editing timers and variables and then importing xml file
        """
        selected_indexes_list = [self.model().get_data_node(index) for index in self.selectionModel().selectedIndexes()]
        if len(selected_indexes_list) == 0:
            selected_indexes_list = [0]
        has_opc_device = False
        # has_folder = False
        has_variable = False
        if isinstance(selected_indexes_list[0], OPCDevice):
            # has_folder = True
            has_variable = True
        elif isinstance(selected_indexes_list[0], opcua.common.node.Node):
            # has_folder = True
            has_variable = True
        elif isinstance(selected_indexes_list[0], str):
            has_variable = True
        elif isinstance(selected_indexes_list[0], int):
            has_opc_device = True

        if has_opc_device:
            add_opc_device = QAction("Add OPC Device", self)
            add_opc_device.triggered.connect(self.add_device)
            context.addAction(add_opc_device)
        # if has_folder:
        #     add_folder = QAction("Add Folder", self)
        #     add_folder.triggered.connect(self.add_folder)
        #     context.addAction(add_folder)
        if has_variable:
            add_variable = QAction("Add Variable", self)
            add_variable.triggered.connect(self.add_variable)
            context.addAction(add_variable)
        """

        delete_node_action = QAction("Delete Device", self)
        delete_node_action.triggered.connect(self.delete_device)
        context.addAction(delete_node_action)

        context.exec(event.globalPos())

    def delete_device(self):
        selected_indexes_list = [self.model().get_data_node(index) for index in self.selectionModel().selectedIndexes()]
        indices = [(index.row(), index.column()) for index in self.selectionModel().selectedIndexes()]
        if len(selected_indexes_list) == 0:
            return
        if isinstance(selected_indexes_list[0], OPCDevice):
            selected_indexes_list[0].delete_all()
            self.model().removeRows(indices[0][0], 1, self)

    def add_device(self):
        print('add_device')
        text, ok = QInputDialog().getText(self, "Device Name", "Device Name:", QLineEdit.Normal)
        if ok and text:
            print(text)
            opcua_server = self.parent().parent().parent().opcua_server
            device = OPCDevice(opcua_server.opcua_server, opcua_server.idx, text)
            device_node = qtree_node_model.OPCUAInfoNode(device)
            self.add_data(device_node)
        for index in self.selectionModel().selectedIndexes():
            print(type(self.model().get_data_node(index)))

    def add_folder(self):
        print('add_folder')
        for index in self.selectionModel().selectedIndexes():
            print(type(self.model().get_data_node(index)))

    def add_variable(self):
        # TODO: Will need a specialized dialog for adding variables because we will need to tie it to a timer, have
        # default values, datatypes, and historized (?)
        text, ok = QInputDialog().getText(self, "Variable Path and Name", "Variable:", QLineEdit.Normal)
        if not (text or ok):
            return
        for index in self.selectionModel().selectedIndexes():
            node = self.model().get_data_node(index)
            if isinstance(node, OPCDevice):
                print(node.name, node.variables)
                node.add_variable(text, 0, data_types.data_types['float'])
            else:
                print(type(node))

    def add_data(self, data):
        model = self.model()
        model.add_child(data, None)
        model.layoutChanged.emit()



import opcua
from PySide6 import QtCore, QtWidgets, Qt
from PySide6.QtGui import QContextMenuEvent, QAction
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QInputDialog, QLineEdit
import qtree_node_model
from opcua_server import OPCUAServer, OPCDevice
import data_types
import value_function_classes


class DeviceTree(QtWidgets.QTreeView):
    remove_function = Signal(value_function_classes.ValueFunction)
    add_function = Signal(value_function_classes.ValueFunction)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(qtree_node_model.OPCUAInfoModel([]))
        self.setWindowTitle("test")

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        context = QtWidgets.QMenu(self)
        selected_indexes_list = [self.model().get_data_node(index) for index in self.selectionModel().selectedIndexes()]
        if len(selected_indexes_list) == 0:
            selected_indexes_list = [0]
        show_plot = False
        if isinstance(selected_indexes_list[0], str):
            show_plot = True
        if show_plot:
            node = selected_indexes_list[1]
            path_pieces = [x.replace('0:', '').replace('2:', '') for x in node.get_path(as_string=True)]
            base = '[' + path_pieces[2] + ']'
            full_path = base + '/'.join(path_pieces[3:])
            t = selected_indexes_list[2]
            f = t.get_function(full_path)

            show_plot_action = QAction("Show Plot", self)
            show_plot_action.triggered.connect(lambda sp: self.show_plot(f))
            context.addAction(show_plot_action)
            remove_plot_action = QAction("Remove Plot", self)
            remove_plot_action.triggered.connect(lambda rp: self.remove_plot(f))
            context.addAction(remove_plot_action)
        delete_node_action = QAction("Delete Device", self)
        delete_node_action.triggered.connect(self.delete_device)
        context.addAction(delete_node_action)

        context.exec(event.globalPos())

    def remove_plot(self, value_function):
        self.remove_function.emit(value_function)

    def show_plot(self, value_function):
        self.add_function.emit(value_function)

    def delete_device(self):
        selected_indexes_list = [self.model().get_data_node(index) for index in self.selectionModel().selectedIndexes()]
        indices = [(index.row(), index.column()) for index in self.selectionModel().selectedIndexes()]
        if len(selected_indexes_list) == 0:
            return
        if isinstance(selected_indexes_list[0], OPCDevice):
            selected_indexes_list[0].delete_all()
            self.model().removeRows(indices[0][0], 1, self)

    def add_data(self, data):
        model = self.model()
        model.add_child(data, None)
        model.layoutChanged.emit()



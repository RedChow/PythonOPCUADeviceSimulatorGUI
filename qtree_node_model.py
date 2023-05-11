import opcua
from opcua import ua
from PySide6 import QtCore
from PySide6.QtCore import QModelIndex
import opcua_server
from timer_class import OPCTimer
from math import modf
"""
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
'__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', 
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
'_browse_next', '_fill_delete_reference_item', '_get_path', '_make_relative_path', 'add_data_type', 'add_folder', 
'add_method', 'add_object', 'add_object_type', 'add_property', 'add_reference', 'add_reference_type', 'add_variable', 
'add_variable_type', 'basenodeid', 'call_method', 'delete', 'delete_reference', 'get_access_level', 
'get_array_dimensions', 'get_attribute', 'get_attributes', 'get_browse_name', 'get_child', 'get_children', 
'get_children_descriptions', 'get_data_type', 'get_data_type_as_variant_type', 'get_data_value', 'get_description', 
'get_description_refs', 'get_display_name', 'get_encoding_refs', 'get_event_notifier', 'get_methods', 
'get_node_class', 'get_parent', 'get_path', 'get_properties', 'get_referenced_nodes', 'get_references', 
'get_type_definition', 'get_user_access_level', 'get_value', 'get_value_rank', 'get_variables', 'history_read', 
'history_read_events', 'nodeid', 'read_event_history', 'read_raw_history', 'register', 'server', 
'set_array_dimensions', 'set_attr_bit', 'set_attribute', 'set_data_value', 'set_event_notifier', 'set_modelling_rule', 
'set_read_only', 'set_value', 'set_value_rank', 'set_writable', 'unregister', 'unset_attr_bit']
"""


class OPCUAInfoNode:
    def __init__(self, data):
        # [name, variable, timer, '']
        self._data = data
        if isinstance(data, tuple):
            self._data = list(data)
        if isinstance(data, str) or not hasattr(data, '__getitem__'):
            self._data = [data]
        self._column_count = len(self._data)
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        if 0 <= column < len(self._data):
            d = self._data[column]
            if isinstance(d, opcua_server.OPCDevice):
                if column == 0:
                    return '{0}'.format(d.name)
            elif isinstance(d, opcua.common.node.Node):
                node_class = d.get_node_class()
                if column == 0:
                    return '{0}'.format(d.get_display_name().to_string())
                elif column == 1 and node_class == 2:
                    display = '{0}'.format(d.get_value())
                    return display
                elif column == 1:
                    return '{0}'.format(node_class)
                else:
                    return 'no data'
            elif isinstance(d, OPCTimer):
                return d.name
            else:
                if column == 3:
                    d = self._data[2]
                    millis = d.interval()
                    if millis == 0:
                        millis = d.interval_milliseconds
                    seconds, minutes = modf(millis/(1000*60))
                    millis, seconds = modf(60*seconds)
                    millis = int(millis*1000)
                    return f'{minutes:02.0f}:{seconds:02.0f}.{millis:03.0f}'
                else:
                    return d
            return self._data[column]

    def get_opc_node(self, column):
        if 0 <= column < len(self._data):
            return self._data[column]

    def column_count(self):
        return self._column_count

    def child_count(self):
        return len(self._children)

    def child(self, row):
        if 0 <= row < self.child_count():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def add_child(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)
        self._column_count = max(child.column_count(), self._column_count)

    def get_children(self):
        return self._children

    def get_data(self):
        return self._data

    def get_all_children_data(self, a=[], d=[]):
        all_children = a
        children_data = d
        for child in self._children:
            if child.child_count() == 0:
                children_data.append(child.get_data())
                all_children.append(child)
            else:
                child.get_all_children_data(all_children, children_data)
        return children_data

    def __del__(self):
        pass


class OPCUAInfoModel(QtCore.QAbstractItemModel):
    def __init__(self, nodes):
        QtCore.QAbstractItemModel.__init__(self)
        self._root = OPCUAInfoNode(None)
        for node in nodes:
            self._root.add_child(node)

    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().child_count()
        return self._root.child_count()

    def removeRows(self, row: int, count: int, parent) -> bool:
        self.beginRemoveRows(QModelIndex(), row, row + count)
        children_data = self._root.get_children()[row].get_all_children_data()
        [x[2].remove_function_by_name(x[1].nodeid.Identifier) for x in children_data]
        del self._root.get_children()[row]
        self.endRemoveRows()
        return True

    def add_child(self, node, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()
        parent.add_child(node)

    def index(self, row, column, _parent=None):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()
        if not QtCore.QAbstractItemModel.hasIndex(self, row, column, _parent):
            return QtCore.QModelIndex()
        child = parent.child(row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def columnCount(self, index):
        if index.isValid():
            return index.internalPointer().column_count()
        return self._root.column_count()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data(index.column())
        return None

    @staticmethod
    def get_data_node(index):
        if not index.isValid():
            return None
        node = index.internalPointer()
        return node.get_opc_node(index.column())

    def update_data(self):
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...):
        headers = ['Device', 'Value', 'Timer', 'Next Update']
        if section < len(headers) and role == QtCore.Qt.DisplayRole:
            return headers[section]



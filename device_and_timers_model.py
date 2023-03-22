from PySide6.QtCore import QAbstractTableModel, Qt, SIGNAL, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit, QComboBox
import value_function_classes
import data_types


class DevicesModel(QAbstractTableModel):
    """
    [device name, variable path, timer, datatype, function, func_arg_1, ..., func_arg_5, writable, historize]
    """
    def __init__(self, data):
        super().__init__()
        if data is None:
            data = []
        self.devices_data = data
        self.timer_names = []
        self.headers = ["Path", "Variable Name", "Datatype", "Timer", "Function", "Arg 1", "Arg 2", "Arg 3", "Arg 4",
                        "Arg 5"]

    def data(self, index, role: int = ...):
        if role == Qt.DisplayRole:
            if index.column() == 2:
                return self.devices_data[index.row()][index.column()].name
            return self.devices_data[index.row()][index.column()]
        elif role == Qt.ToolTipRole:
            if index.column() == 4:
                function_type = self.devices_data[index.row()][index.column()]
                tool_tip = ''
                if function_type == 'valuelist':
                    tool_tip = "Arg 1: Values to iterate through<br>" \
                               "Arg 2: Number of times to repeat through list.<br>" \
                               "Arg 3: Repeat forever (True/False)<br>" \
                               "Arg 4: Historize (not working)<br>" \
                               "Arg 5: Not used"
                elif function_type == 'weightedlist':
                    tool_tip = "Arg 1: Values to iterate through [v_1, ..., v_n]<br>" \
                               "Arg 2: Weights [w_1, ...,w_n]<br>" \
                               "Arg 3: Number of times to call a random sample<br>" \
                               "Arg 4: Repeat forever (True/False)<br>" \
                               "Arg 5: Historize (not working)<br>" \
                               "Random sample is taken from w_1 copies of v_1, ..., w_n copes of v_n"
                elif function_type == 'rampstep':
                    tool_tip = "Arg 1: Minimum y value<br>" \
                               "Arg 2: Maximum y value<br>" \
                               "Arg 3: Step added to y every evaluation call<br>" \
                               "Arg 4: Repeat forever (True/False)<br>" \
                               "Arg 5: Historize (not working)"
                else:
                    tool_tip = "Arg 1: Minimum y value<br>" \
                               "Arg 2: Maximum y value<br>" \
                               "Arg 3: How long in seconds to repeat<br>" \
                               "Arg 4: Repeat forever (True/False)<br>" \
                               "Arg 5: Historize (not working)"
                    if 'square' in function_type:
                        tool_tip += "<br>Oscillates between min and max."
                return tool_tip

    def rowCount(self, index):
        return len(self.devices_data)

    def columnCount(self, index):
        if len(self.devices_data) > 0:
            return len(self.devices_data[0])
        return 0

    def update_timer_names(self, timer_names):
        self.timer_names.extend(timer_names)

    def flags(self, index):
        if not index.isValid():
            return 0
        if index.column() in range(0, 11):
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section: int, orientation, role: int = ...):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft|Qt.AlignCenter)
            return int(Qt.AlignRight|Qt.AlignCenter)
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if 0 <= section < len(self.headers):
                    return self.headers[section]

    def setData(self, index, value, role: int = ...) -> bool:
        if index.isValid() and 0 <= index.row() < len(self.devices_data):
            if index.column() == 2:
                self.devices_data[index.row()][index.column()] = data_types.data_types[value]
            else:
                self.devices_data[index.row()][index.column()] = value
        return True

    def add_device(self):
        self.devices_data.append(['']*len(self.devices_data[0]))


class DeviceDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(DeviceDelegate, self).__init__(parent)
        # print(parent.timer_names)
        self.timer_names = parent.timer_names
        vf = value_function_classes.ValueFunction(None, None, None, None, None)
        self.function_list = vf.functions()

    def update_timer_names(self, timer_names):
        self.timer_names = timer_names

    def createEditor(self, parent, option, index):
        if index.column() in [0, 1, 5, 6, 7, 8, 9]:
            editor = QLineEdit(parent)
            editor.setText("Timer Name")
            return editor
        elif index.column() == 2:
            editor = QComboBox(parent)
            editor.addItems(sorted([key for key in data_types.data_types]))
            return editor
        elif index.column() == 3:
            editor = QComboBox(parent)
            editor.addItems(sorted(self.timer_names))
            return editor
        elif index.column() == 4:
            editor = QComboBox(parent)
            editor.addItems(sorted(self.function_list))
            return editor

    def commit_and_close_editor(self):
        editor = self.sender()

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        if index.column() == 0:
            editor.setText(text.replace('\\', '/'))
        elif index.column() in [1, 5, 6, 7, 8, 9]:
            editor.setText(text)
        elif index.column() in [2, 3, 4]:
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)

    def setModelData(self, editor, model, index) -> None:
        if index.column() == 0:
            model.setData(index, editor.text().replace('\\', '/'))
        elif index.column() in [1, 5, 6, 7, 8, 9]:
            model.setData(index, editor.text())
        elif index.column() in [2, 3, 4]:
            model.setData(index, editor.currentText())


class TimersModel(QAbstractTableModel):
    timer_changed = Signal(int)

    def __init__(self, data):
        super().__init__()
        if data is None:
            data = []
        self.timer_data = data

    def flags(self, index):
        if not index.isValid():
            return 0
        if index.column() in range(0, 5):
            v = Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return v
        else:
            v = Qt.ItemIsSelectable | Qt.ItemIsEnabled
            return v

    def data(self, index, role: int = ...):
        if role == Qt.DisplayRole:
            timer_type = self.timer_data[index.row()][1]
            if timer_type == 'random':
                if index.column() != 4:
                    return self.timer_data[index.row()][index.column()]
                return ''
            elif timer_type == 'periodic':
                if index.column() in [0, 1, 4]:
                    return self.timer_data[index.row()][index.column()]
                return ''
        elif role == Qt.BackgroundRole:
            timer_type = self.timer_data[index.row()][1]
            if timer_type == 'random':
                if index.column() == 4:
                    return QColor(30, 30, 30)
            elif timer_type == 'periodic':
                if index.column() in [2, 3]:
                    return QColor(30, 30, 30)
        elif role == Qt.ToolTipRole:
            if index.column() == 1:
                return "Random timers evaluate at a random time in seconds between min and max. Periodic timers " \
                       "evaluate at a constant rate of time."

    def rowCount(self, index) -> int:
        return len(self.timer_data)

    def columnCount(self, index):
        if len(self.timer_data) > 0:
            return len(self.timer_data[0])
        return 0

    def headerData(self, section: int, orientation, role: int = ...):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return int(Qt.AlignLeft|Qt.AlignCenter)
            return int(Qt.AlignRight|Qt.AlignCenter)
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Name"
                elif section == 1:
                    return "Type"
                elif section == 2:
                    return "Random Min"
                elif section == 3:
                    return "Random Max"
                elif section == 4:
                    return "Periodic Timeout"

    def setData(self, index, value, role: int = ...) -> bool:
        print(index.row(), index.column(), value, role)
        if index.isValid() and 0 <= index.row() < len(self.timer_data):
            if index.column() == 0:
                self.timer_data[index.row()][0] = value
                self.timer_changed.emit(index.row())
        return True

    def add_timer(self):
        self.timer_data.append(['']*len(self.timer_data[0]))


class TimerDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(TimerDelegate, self).__init__(parent)
        self.timer_data = parent.timers_model.timer_data

    def createEditor(self, parent, option, index):
        timer_type = ''
        if index.row() < len(self.timer_data):
            timer_type = self.timer_data[index.row()][1]
        if index.column() == 0:
            editor = QLineEdit(parent)
            editor.setText("Timer Name")
            self.connect(editor, SIGNAL("returnPressed()"), self.commit_and_close_editor)
            return editor
        elif index.column() == 1:
            editor = QComboBox(parent)
            editor.addItems(['periodic', 'random'])
            return editor
        elif index.column() == 2 and timer_type == 'random':
            editor = QLineEdit(parent)
            editor.setText("Min (sec)")
            return editor
        elif index.column() == 3 and timer_type == 'random':
            editor = QLineEdit(parent)
            editor.setText("Max (sec)")
            return editor
        elif index.column() == 4 and timer_type == 'periodic':
            editor = QLineEdit(parent)
            editor.setText("timeout (sec)")
            return editor

    def commit_and_close_editor(self):
        pass

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        if index.column() in [0, 2, 3, 4]:
            editor.setText(text)
        elif index.column() in [1]:
            i = editor.findText(text)
            if i == -1:
                i = 0
            editor.setCurrentIndex(i)

    def setModelData(self, editor, model, index) -> None:
        if index.column() == 0:
            model.setData(index, editor.text())

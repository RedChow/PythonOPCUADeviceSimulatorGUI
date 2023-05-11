import pyqtgraph
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal, Slot
import value_function_classes


class PyQtGraphHistory:
    def __init__(self, plot_widget):
        print('we made it')
        self.plot_widget = plot_widget
        self.function_list = []
        self.curve_dict = {}

    def remove_function(self, function):
        try:
            i = self.function_list.index(function)
            self.plot_widget.removeItem(self.curve_dict[function.get_full_path()])
            del self.curve_dict[function.get_full_path()]
        except ValueError:
            pass
        else:
            del self.function_list[i]

    def add_function(self, function):
        if function in self.function_list:
            return
        self.function_list.append(function)
        function.new_data.connect(self.update_data)
        self.curve_dict[function.get_full_path()] = pyqtgraph.PlotCurveItem()
        self.update_curve_data(function)

    @Slot(str)
    def update_data(self, path):
        try:
            i = self.function_list.index(path)
        except ValueError:
            return
        else:
            f = self.function_list[i]
            self.update_curve_data(f)

    def update_curve_data(self, function):
        x_values, y_values = function.get_plot_values()
        path = function.get_full_path()
        if x_values is not None and y_values is not None:
            curve_item = self.curve_dict[path]
            self.plot_widget.removeItem(curve_item)
            curve_item.setData(x_values, y_values)
            self.plot_widget.addItem(curve_item)
            self.curve_dict[path] = curve_item


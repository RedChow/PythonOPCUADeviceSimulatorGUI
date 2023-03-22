from lxml import etree
from opcua_server import OPCDevice
import data_types
import timer_class
import value_function_classes
from qtree_node_model import OPCUAInfoNode
from logging import config
import logging
import ast
import glob


config.fileConfig("log_conf.conf")
logger = logging.getLogger('main')


class XMLParser:
    def __init__(self, opcua_server_instance, parent=None):
        self.opcua_server = opcua_server_instance
        self.parent = parent
        self.timer_instances = []
        self.timer_model_data = []
        self.device_model_data = []
        self.opcua_paths_and_nodes = []
        self.device_node = None
        self.opc_device = None
        self.pathname = ''
        self.used_device_names = []

    def parse_directory(self, directory_path):
        for self.pathname in sorted(glob.glob(directory_path + '/*.xml')):
            # document = etree.parse(self.pathname)
            # self.parse_file(document)
            # print(self.pathname)
            self.parse_file(self.pathname)

    def parse_file(self, file_path):
        xml = etree.parse(file_path)
        # Get timers first since variables depend on having a timer defined
        for node in xml.xpath("//timers/timer"):
            self.parse_timer_node(node, file_path)
        for node in xml.xpath("//device"):
            device_name = node.attrib.get('name')
            if device_name in self.used_device_names:
                logger.warning(f"Device already named {device_name} exists. Skipping device in {file_path}.")
                continue
            self.used_device_names.append(device_name)
            if not device_name:
                logger.warning(f'Device element has no name attribute in {file_path}. Device will not be used.')
                continue
            if self.opcua_server is not None:
                self.opc_device = OPCDevice(self.opcua_server.opcua_server, self.opcua_server.idx, device_name)
            self.recursive_parse(node, '//device', device_name, device_name)
            if self.opcua_server is not None:
                device_node = OPCUAInfoNode(self.opc_device)
                # print(device_node)
                for p in self.opc_device.qtree_widget_items:
                    if self.opc_device.qtree_widget_items[p].parent() is None:
                        device_node.add_child(self.opc_device.qtree_widget_items[p])
                if device_node.child_count() > 0:
                    self.opcua_paths_and_nodes.append(device_node)

    def parse_timer_node(self, node, file_path):
        try:
            timer_name = node.findall('name')[0].text
            timer_type = node.findall('type')[0].text
        except IndexError:
            logger.warning(f"Error in getting name and timer type in {file_path}. Timer will not be used.")
            return
        qtimer = None
        timer_data = [timer_name, timer_type]
        if timer_type == 'random':
            try:
                timer_min = float(node.findall('min')[0].text)
                timer_max = float(node.findall('max')[0].text)
                timer_data.extend([timer_min, timer_max, 0])
                if self.opcua_server is not None:
                    qtimer = timer_class.OPCTimer(None)
                    qtimer.set_name(timer_name)
                    qtimer.set_timer_type(timer_type)
                    qtimer.set_min_max(timer_min, timer_max)
            except IndexError:
                logger.warning(f"No min or max set for random timer name {timer_name} in file {self.pathname}. "
                               f"Timer will not work. Discarding timer data.")
                return
        elif timer_type == 'periodic':
            try:
                timer_timeout = int(float(node.findall('timeout')[0].text)) * 1000
                timer_data.extend([0, 0, timer_timeout])
                if self.opcua_server is not None:
                    qtimer = timer_class.OPCTimer(None)
                    qtimer.set_name(timer_name)
                    qtimer.set_timer_type(timer_type)
                    qtimer.set_interval(timer_timeout)
            except IndexError:
                logger.warning(f"No timeout set for period timer {timer_name} in file {self.pathname}. "
                               f"Timer will not work. Discarding timer data")
                return
            # print(f'Adding qtimer {timer_timeout}, {qtimer.interval()}')
        else:
            logger.warning(f"No timer type found for {timer_name} in file {self.pathname}. Discarding timer data.")
            return
        if timer_name not in self.timer_instances and qtimer is not None:
            self.timer_instances.append(qtimer)
        if self.opcua_server is None:
            if timer_name not in [x[0] for x in self.timer_model_data]:
                self.timer_model_data.append(timer_data)

    def parse_and_create_function(self, node, variable_name, variable_datatype, variable_timer, root_path):
        try:
            i = self.timer_instances.index(variable_timer)
        except ValueError:
            logger.warning(f"Timer {variable_timer} not defined before use.")
            return
        else:
            qtimer = self.timer_instances[i]
        function_type = None
        try:
            function_type = node.findall('type')[0].text.lower()
        except IndexError:
            return None
        if function_type is None:
            return None
        value_function = value_function_classes.ValueFunction(None, None, None, None, None)
        func_dict = value_function.get_function_list(function_type)
        function_parameters = {}
        for func_arg in func_dict:
            try:
                function_parameters[func_dict[func_arg]] = node.findall(func_dict[func_arg])[0].text
            except IndexError:
                # logger.warning(f"No function defined. {func_arg}...{func_dict}")
                pass
        # print(variable_name, variable_timer, function_parameters, function_type)
        f = None
        try:
            v_path = root_path + '/' + variable_name
            period = 0
            if 'period' in function_parameters:
                period = int(function_parameters['period'])
            repeat = True
            if 'repeat' in function_parameters:
                repeat = True if function_parameters['repeat'].lower() == 'true' else False
            historize = False
            if 'historize' in function_parameters:
                historize = True if function_parameters['historize'].lower() == 'true' else False
            if function_type == 'weightedlist':
                f = value_function_classes.WeightedList(self.opc_device, v_path, 0, 0,
                                                        period,
                                                        ast.literal_eval(function_parameters['values']),
                                                        ast.literal_eval(function_parameters['weights']),
                                                        repeat, historize)
            elif function_type == 'triangle':
                f = value_function_classes.Triangle(self.opc_device, v_path, float(function_parameters['min']),
                                                        float(function_parameters['max']), 1000*period,
                                                        repeat, historize)
            elif function_type == 'rampstep':
                f = value_function_classes.RampStep(self.opc_device, v_path, float(function_parameters['min']),
                                                    float(function_parameters['max']),
                                                    float(function_parameters['step']),
                                                    repeat, historize)
            elif function_type == 'rampperiodic':
                f = value_function_classes.RampPeriodic(self.opc_device, v_path, float(function_parameters['min']),
                                                        float(function_parameters['max']),
                                                        period*1000,
                                                        repeat, historize)
            elif function_type == 'square':
                f = value_function_classes.Square(self.opc_device, v_path, float(function_parameters['min']),
                                                    float(function_parameters['max']), 1000*period,
                                                    repeat, historize)
            elif function_type == 'randomsquare':
                f = value_function_classes.RandomSquare(self.opc_device, v_path, float(function_parameters['min']),
                                                    float(function_parameters['max']), 1000*period,
                                                    repeat, historize)
            elif function_type == 'sin':
                f = value_function_classes.Sin(self.opc_device, v_path, float(function_parameters['min']),
                                                    float(function_parameters['max']), 1000*period,
                                                    repeat, historize)
            elif function_type == 'cos':
                f = value_function_classes.Cos(self.opc_device, v_path, float(function_parameters['min']),
                                                    float(function_parameters['max']), 1000*period,
                                                    repeat, historize)
            elif function_type == 'valuelist':
                f = value_function_classes.ValueList(self.opc_device, v_path,
                                                     ast.literal_eval(function_parameters['values']),
                                                     period,
                                                     repeat,
                                                     historize)
            elif function_type == 'ramprandom':
                f = value_function_classes.RampRandom(self.opc_device, v_path, float(function_parameters['min']),
                                                      float(function_parameters['max']), 0,
                                                      ast.literal_eval(function_parameters['bounds']), repeat,
                                                      historize)
        except ValueError:
            logger.warning(f"Error in parsing function for {variable_name} in file {self.pathname}. Variable will not"
                           f"be used.")
        else:
            # print(f)
            if f is not None:
                full_path = root_path + '/' + variable_name
                full_path = full_path[full_path.index('/') + 1:]
                # print(full_path)
                self.opc_device.add_variable(full_path, 0, variable_datatype, True, qtimer)
                qtimer.add_function(f)

    def parse_variable_node(self, node, root_path):
        try:
            variable_name = node.findall('name')[0].text
            variable_datatype = node.findall('datatype')[0].text.lower()
            variable_datatype_ua = data_types.data_types.get(variable_datatype, '')
            variable_timer = node.findall('timer')[0].text
        except IndexError:
            logger.warning(f"Error in parsing name, datatype, timer, or function elements in file "
                           f"{self.pathname}. Discarding variable.")
            return
        # print(variable_name, variable_timer, variable_datatype)
        try:
            next_node = node.findall('function')[0]
        except IndexError:
            logger.error(f"No function tag for {variable_name} in {root_path}. Will not add variable.")
            return

        try:
            path_tag = node.findall('path')[0].text
            path_base = path_tag.split('/')[0]
        except IndexError:
            pass
        except AttributeError:
            path_base = ''
            path_tag = ''
        else:
            base_path = root_path.split('/')[0]
            if path_base != base_path:
                path_tag = base_path + '/' + path_tag
            root_path = path_tag
        if self.opcua_server is not None:
            self.parse_and_create_function(next_node, variable_name, variable_datatype_ua, variable_timer, root_path)
            """
            try:
                self.parse_and_create_function(node.findall('function')[0], variable_name, variable_datatype_ua,
                                           variable_timer, root_path)
            except IndexError:
                logger.warning(f"No function defined for {variable_name} in {self.pathname}. Variable will not be"
                               f" used.")
            """
        else:
            """
            try:
                self.parse_function_node(node.findall('function')[0], variable_name, variable_datatype, variable_timer,
                                     root_path)
            except IndexError:
                logger.warning(f"No function defined for {variable_name} in {self.pathname}. Variable will not be"
                               f" used.")
            """
            self.parse_function_node(next_node, variable_name, variable_datatype_ua, variable_timer, root_path)

    def parse_function_node(self, node, variable_name, variable_datatype, variable_timer, root_path):
        value_function = value_function_classes.ValueFunction(None, None, None, None, None)
        function_type = node.findall('type')[0].text.lower()
        # print(function_type)
        func_dict = value_function.get_function_list(function_type)
        reversed_dict = {value: key for (key, value) in func_dict.items()}
        reversed_dict_holder = reversed_dict
        for key in reversed_dict:
            try:
                reversed_dict_holder[key] = node.findall(key)[0].text
            except IndexError:
                if key == 'historize':
                    reversed_dict[key] = False
                else:
                    reversed_dict[key] = ''
        function_data = [root_path, variable_name, variable_datatype, variable_timer, function_type] + \
                        [reversed_dict[func_dict[key]] for key in sorted(func_dict.keys())]
        # valuelist only has func_arg_1 through func_arg_4
        if len(function_data) != 10:
            function_data = function_data + ['']*(10-len(function_data))
        self.device_model_data.append(function_data)

    def recursive_parse(self, node, x_path, p_name, root_path):
        # print(node, p_name, f"{x_path}[@name={p_name}]", root_path)
        for root_node in node.xpath(f"{x_path}[@name='{p_name}']"):
            # print('root_node', root_node)
            for child in root_node.getchildren():
                if child.tag == 'folder':
                    self.recursive_parse(child, f"{x_path}[@name='{p_name}']" + '//folder', child.attrib.get('name'), root_path + '/' + child.attrib.get('name'))
                elif child.tag == 'variable':
                    self.parse_variable_node(child, root_path)
                    # print('after parse_variable_node', p_name, root_path)


class XMLCreator:
    def __init__(self, full_path):
        self.pathname = full_path

    def write_data_to_file(self, timers, devices):
        """
        :param timers:
            list of dictionaries that have keys 'name', 'type', and either 'timeout' or 'min' and 'max'
        :param devices:
            list dictionaries with keys 'name' and 'variables'
            NOTE: 'variables' is a dictionary with keys 'path', 'function', 'datatype', 'timer', 'func_arg_1',
                'func_arg_2', 'func_arg_3', 'func_arg_4', 'func_arg_5'
                The func_arg_n will depend on the function.
        :return:
            True if file was written with no exceptions
            False otherwise
        """
        document = etree.Element("simulator")
        sub_element_timers = etree.SubElement(document, "timers")
        for timer in timers:
            timer_element = etree.SubElement(sub_element_timers, "timer")
            for key in timer:
                key_sub_element = etree.SubElement(timer_element, key)
                key_sub_element.text = f"{timer[key]}"

        for device in devices:
            try:
                device_element = etree.SubElement(document, "device")
                device_element.set("name", device["name"])
                for variable in device["variables"]:
                    v = etree.SubElement(device_element, "variable")
                    if v is not None:
                        path_parts = variable['path'].split('/')
                        v_name = etree.SubElement(v, "name")
                        v_name.text = path_parts[-1]
                        v_datatype = etree.SubElement(v, "datatype")
                        v_datatype.text = variable['datatype']
                        v_timer = etree.SubElement(v, "timer")
                        v_timer.text = variable['timer']
                        v_path = etree.SubElement(v, "path")
                        v_path.text = '/'.join(path_parts[:-1])
                        function_element = etree.SubElement(v, "function")
                        function_type = etree.SubElement(function_element, "type")
                        function_type.text = variable['function']
                        value_function = value_function_classes.ValueFunction(None, None, None, None, None)
                        func_dict = value_function.get_function_list(variable['function'])
                        for func_arg in func_dict:
                            func_element = etree.SubElement(function_element, f"{func_dict[func_arg]}")
                            func_element.text = f"{variable[func_arg]}"
            except KeyError:
                return False
        try:
            root = etree.ElementTree(document)
            root.write(f'{self.pathname}', pretty_print=True, xml_declaration=True, encoding="utf-8")
        except Exception as e:
            logger.error(f"Error writing to {self.pathname}. Error message: {e.message}")
            return False
        else:
            return True

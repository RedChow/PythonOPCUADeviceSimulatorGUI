import sys
from opcua import ua, Server, uamethod
from logging import config
import logging
from qtree_node_model import OPCUAInfoNode
from PySide6.QtCore import QObject, Signal

sys.path.insert(0, "..")

config.fileConfig("log_conf.conf")
logger = logging.getLogger('main')


"""
'__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
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


class OPCDevice:
    def __init__(self, server, idx, name):
        self.server = server
        self.idx = idx
        self.name = name
        self.variables = []
        self.opc_folders = {}
        self.opc_path_hashmap = {}
        self.qtree_widget_items = {}
        object_node = self.server.get_objects_node()
        self.var_object = object_node.add_object('ns=2;s=[{}]'.format(name), name)

    def delete_all(self):
        # print(dir(self.var_object))
        for folder in self.opc_path_hashmap:
            self.opc_path_hashmap[folder].delete()
        self.var_object.delete()
        self.variables = []

    def add_variable(self, full_path, default_value, data_type, writable=True, timer=None):
        folder_path, name = self.parse_variable_path(full_path)
        if folder_path and name:
            variable = self.opc_folders[folder_path].add_variable('ns=2;s=[{0}]{1}/{2}'.format(self.name,
                                                                  folder_path, name), name,
                                                                  default_value, data_type)
            node = OPCUAInfoNode([name, variable, timer, ''])
            self.qtree_widget_items[folder_path].add_child(node)

            if writable:
                variable.set_writable()
        else:
            variable = self.var_object.add_variable('ns=2;s=[{0}]{1}'.format(self.name, name), name, default_value,
                                                    data_type)
            self.qtree_widget_items[name] = OPCUAInfoNode([name, variable, timer, ''])
        hash_path = folder_path + '/' + name
        if not folder_path:
            hash_path = name
        self.opc_path_hashmap[hash_path] = variable

    def parse_variable_path(self, path):
        path_parts = path.split('/')
        if len(path_parts) == 1:
            return '', path
        if path_parts[0] not in self.opc_folders:
            self.opc_folders[path_parts[0]] = self.var_object.add_folder(self.idx, path_parts[0])
            self.qtree_widget_items[path_parts[0]] = OPCUAInfoNode(self.opc_folders[path_parts[0]])
        for i, current in enumerate(path_parts[1:-1]):
            base = '/'.join(path_parts[0:i+1])
            new_path = base + '/' + current
            if new_path not in self.opc_folders:
                self.opc_folders[base + '/' + current] = self.opc_folders[base].add_folder(self.idx, current)
                # node = OPCUAInfoNode(current)
                node = OPCUAInfoNode(self.opc_folders[new_path])
                self.qtree_widget_items[base].add_child(node)
                self.qtree_widget_items[new_path] = node
        return '/'.join(path_parts[:-1]), path_parts[-1]

    def set_value(self, path, value):
        try:
            self.opc_path_hashmap[path].set_value(value)
        except KeyError:
            return -1

    def get_value(self, path):
        try:
            return self.opc_path_hashmap[path].get_value()
        except ValueError:
            return None

    def __eq__(self, other):
        return other == self.name

    def __repr__(self):
        return self.name

    def __del__(self):
        print('I have been deleted...')


"""
'__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', 
'__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', 
'__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', 
'__subclasshook__', '__weakref__', '_application_uri', '_create_custom_type', '_policies', '_policyIDs', 
'_security_policy', '_set_endpoints', '_setup_server_nodes', 'allow_remote_admin', 'application_type', 'bserver', 
'certificate', 'create_custom_data_type', 'create_custom_event_type', 'create_custom_object_type', 
'create_custom_variable_type', 'create_subscription', 'default_timeout', 'dehistorize_node_data_change', 
'dehistorize_node_event', 'delete_nodes', 'disable_clock', 'endpoint', 'export_xml', 'export_xml_by_ns', 
'find_servers', 'get_application_uri', 'get_endpoints', 'get_event_generator', 'get_namespace_array', 
'get_namespace_index', 'get_node', 'get_objects_node', 'get_root_node', 'get_server_node', 
'historize_node_data_change', 'historize_node_event', 'import_xml', 'iserver', 'link_method', 'load_certificate', 
'load_enums', 'load_private_key', 'load_type_definitions', 'local_discovery_service', 'logger', 'manufacturer_name', 
'name', 'nodes', 'private_key', 'product_uri', 'register_namespace', 'set_application_uri', 'set_attribute_value', 
'set_build_info', 'set_endpoint', 'set_security_IDs', 'set_security_policy', 'set_server_name', 'start', 'stop', 
'subscribe_server_callback', 'unsubscribe_server_callback', 'user_manager'
"""


class OPCUAServer(QObject):
    start_server_feedback = Signal()

    def __init__(self):
        super().__init__(None)
        self.opcua_server = Server()
        self.idx = None
        self.objects = None
        self.object_list = []
        self.variable_list = []
        self.device_list = []
        self.added_variables = False
        self.address = ''
        self.server_started = False

    def set_address(self, address):
        self.address = address

    def start_server(self):
        try:
            self.opcua_server.set_endpoint(self.address)
            self.idx = self.opcua_server.register_namespace('http://examples.freeopcua.github.io')
            self.opcua_server.start()
        except Exception as e:
            logger.error(f"Could not start OPC-UA server. Error info: {e}")
            self.server_started = False
        else:
            self.server_started = True
        finally:
            self.start_server_feedback.emit()

    def stop_server(self):
        self.opcua_server.stop()

    def update_variable(self, index, new_value):
        self.variable_list[index].set_value(new_value)

    def get_device(self, device_name):
        try:
            i = self.device_list.index(device_name)
        except (IndexError, ValueError):
            return None
        else:
            return self.device_list[i]



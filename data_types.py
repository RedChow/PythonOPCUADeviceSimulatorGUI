from opcua import ua
data_types = {
    'null': ua.VariantType.Null,
    'boolean': ua.VariantType.Boolean,
    'sbyte': ua.VariantType.SByte,
    'byte': ua.VariantType.Byte,
    'int16': ua.VariantType.Int16,
    'uint16': ua.VariantType.UInt16,
    'int32': ua.VariantType.Int32,
    'uint32': ua.VariantType.UInt32,
    'int64': ua.VariantType.Int64,
    'uint64': ua.VariantType.UInt64,
    'float': ua.VariantType.Float,
    'double': ua.VariantType.Double,
    'string': ua.VariantType.String,
    'datetime': ua.VariantType.DateTime,
    'guid': ua.VariantType.Guid,
    'bytestring': ua.VariantType.ByteString,
    'xmlelement': ua.VariantType.XmlElement,
    'nodeid': ua.VariantType.NodeId,
    'expandednodeid': ua.VariantType.ExpandedNodeId,
    'statuscode': ua.VariantType.StatusCode,
    'qualifiedname': ua.VariantType.QualifiedName,
    'localizedtext': ua.VariantType.LocalizedText,
    'extensionobject': ua.VariantType.ExtensionObject,
    'datavalue': ua.VariantType.DataValue,
    'variant': ua.VariantType.Variant,
    'diagnosticinfo': ua.VariantType.DiagnosticInfo
}


def convert_default(data_type, default_value):
    try:
        if data_type.startswith('int') or data_type.startswith('uint'):
            return int(default_value)
        elif data_type == 'null':
            return None
        elif data_type in ['float', 'double']:
            return float(default_value)
        else:
            return default_value
    except ValueError:
        return default_value




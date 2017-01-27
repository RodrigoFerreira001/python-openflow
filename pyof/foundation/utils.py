"""Helper python-openflow functions."""

# System imports

# Third-party imports

from importlib import import_module
from pyof.foundation.basic_types import UBInt8
from pyof.foundation.constants import PyofVersion


__all__ = ('new_message_from_header', 'new_message_from_message_type',
           'unpack_message')

switch_message_types = {
    'asynchronous': ['error_msg', 'flow_removed', 'packet_in', 'port_status'],
    'controller2switch': ['barrier_reply', 'barrier_request', 'features_reply',
                          'features_request', 'flow_mod', 'get_config_reply',
                          'get_config_request', 'packet_out', 'port_mod',
                          'queue_get_config_reply', 'queue_get_config_request',
                          'set_config', 'stats_reply', 'stats_request'],
    'symmetric': ['echo_reply', 'echo_request', 'hello', 'vendor_header']
}


def get_class_name(message_type_name):
    """Method used to convert message_type_name to class_name.

    e.g. 'error_msg' to 'ErroMsg'

    Parameters:
        message_type_name(string): Name of module_name
    Returns:
        class_name(string): Name of a class based on message_type_name
    """
    return message_type_name.title().replace('_', '')


def get_module_name(message_type):
    """Method used to convert a message_type instance to string with module.

    e.g.    message_type to 'barrier_reply'

    Parameters:
        message_type(Enum): Enum reference from a message type.
    Returns:
        module_name(string): Name of a module based in a message_type given.
    """
    type_name = message_type.enum_ref(message_type).name
    return type_name.replace('OFPT_', '').lower()


def new_message_from_message_type(version, message_type):
    """Method used to build a class based on version and message_type given.

    Parameters:
        version(UBInt8(enum_ref=PyofVersion)): UBInt8 with PyofVersion value.
        message_type(UBInt8(enum_ref=Type)): UBInt with a Type value of the
                                             message given.
    Returns:
        class_from_message(Class): Class based on version and message_type.
    """
    module_name = get_module_name(message_type)

    for module, _types in switch_message_types.items():
        for msg_type in _types:
            if module_name in msg_type:
                module_name = 'pyof.{}.{}.{}'.format(version.name,
                                                     module,
                                                     msg_type)
                message_type_name = get_class_name(msg_type)
                break
    return getattr(import_module(module_name), message_type_name)


def new_message_from_header(header):
    """Given an OF Header, return an empty message of header's message_type.

    Args:
        header (Header): Unpacked OpenFlow Header.

    Returns:
        Empty OpenFlow message of the same type of message_type attribute from
        the given header.
        The header attribute of the message will be populated.

    Raises:
        KytosUndefinedMessageType: Unkown Message_Type.
    """
    version = header.version.enum_ref(header.version.value)
    return new_message_from_message_type(version, header.message_type)()


def unpack_header(buff):
    """Method used to unpack a Header from a given buff."""
    version = UBInt8(enum_ref=PyofVersion)
    version.unpack(buff)
    version = version.enum_ref(version.value)

    header = version.get_header()
    header.unpack(buff)
    return header


def unpack_message(buffer):
    """Unpack the whole buffer, including header pack."""
    header = unpack_header(buffer)
    msg_buff = buffer[header.get_size():]

    message = new_message_from_header(header)
    message.unpack(msg_buff)

    message.header = header
    return message

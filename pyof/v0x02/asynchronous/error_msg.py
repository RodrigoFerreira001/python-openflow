# System imports
from enum import Enum

"""Defines an Error Message."""
from pyof.v0x01.asynchronous.error_msg import (BadActionCode, BadRequestCode,
                                               ErrorMsg, ErrorType,
                                               FlowModFailedCode,
                                               HelloFailedCode,
                                               PortModFailedCode,
                                               QueueOpFailedCode)

__all__ = ('ErrorMsg', 'ErrorType', 'BadActionCode', 'BadRequestCode',
           'FlowModFailedCode', 'HelloFailedCode', 'PortModFailedCode',
           'QueueOpFailedCode')

class ErrorType(Enum):
    """Values for ’type’ in ofp_error_message.

    These values are immutable: they will not change in future versions of the
    protocol (although new values may be added).
    """

    #: Hello protocol failed
    OFPET_HELLO_FAILED = 0
    #: Request was not understood
    OFPET_BAD_REQUEST = 1
    #: Error in action description
    OFPET_BAD_ACTION = 2
    #: Problem in modifying Flow entry
    OFPET_FLOW_MOD_FAILED = 3
    #: New - added in v0x02
    #: Problem modifying group entry
    OFPET_GROUP_MOD_FAILED = 4
    #: Problem in modifying Port entry
    OFPET_PORT_MOD_FAILED = 5
    #: New - added in v0x02
    #: Problem in handling tables
    OFPET_TABLE_MOD_FAILED = 6
    #: Problem in modifying Queue entry
    OFPET_QUEUE_OP_FAILED = 7


class TableModFailed(Enum):
    """Error msg 'code' values for OFPET_QUEUE_OP_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Specified table does not exist
    OFPTMFC_BAD_TABLE = 0,
    #: Specified config does not exist
    OFPTMFC_BAD_CONFIG = 1


class PortModFailedCode(Enum):
    """Error_msg 'code' values for OFPET_PORT_MOD_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Specified port does not exist
    OFPPMFC_BAD_PORT = 0
    #: Specified hardware address is wrong
    OFPPMFC_BAD_HW_ADDR = 1
    #: New - added in v0x02
    #: Specified config is invalid
    OFPPMFC_BAD_CONFIG = 2
    #: New - added in v0x02
    #: Specified advertise is invalid
    OFPPMFC_BAD_ADVERTISE =3


class GroupModFailed(Enum):
    """Error_msg 'code' values for OFPET_GROUP_MOD_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Group already exists
    OFPGMFC_GROUP_EXISTS = 0
    #: Group is invalid
    OFPGMFC_INVALID_GROUP = 1
    #: Switch does not support unequal load sharing with select groups
    OFPGMFC_WEIGHT_UNSUPPORTED = 2
    #: Group table is full
    OFPGMFC_OUT_OF_GROUPS = 3
    #: Max number of action buckets for a group has been exceeded
    OFPGMFC_OUT_OF_BUCKETS = 4
    #: Switch does not support groups that forward to groups
    OFPGMFC_CHAINING_UNSUPPORTED = 5
    #: This group cannot watch the watch_port or watch_group specified
    OFPGMFC_WATCH_UNSUPPORTED = 6
    #: Group entry cause a loop
    OFPGMFC_LOOP = 7
    #: Group no modfied because group doesnt exist
    OFPGMFC_UNKNOWN_GROUP = 8

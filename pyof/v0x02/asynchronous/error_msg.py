# System imports
from enum import Enum

"""Defines an Error Message."""
from pyof.v0x01.asynchronous.error_msg import (BadActionCode, BadRequestCode,
                                               ErrorMsg, ErrorType,
                                               FlowModFailedCode,
                                               HelloFailedCode,
                                               PortModFailedCode,
                                               QueueOpFailedCode)

class ErrorType(Enum):
    """Values for ’type’ in ofp_error_message.

    These values are immutable: they will not change in future versions of the
    protocol (although new values may be added).
    """

    #: Hello protocol failed
    OFPET_HELLO_FAILED = 0,
    #: Request was not understood
    OFPET_BAD_REQUEST = 1,
    #: Error in action description
    OFPET_BAD_ACTION = 2,
    #: Problem in modifying Flow entry
    OFPET_FLOW_MOD_FAILED = 3,
    #: Problem in modifying Port entry
    OFPET_PORT_MOD_FAILED = 4,
    #: New - added in v0x02
    #: Problem in handling tables
    OFPET_TABLE_MOD_FAILED = 5,
    #: Problem in modifying Queue entry
    OFPET_QUEUE_OP_FAILED = 6


class TableModFailed(Enum):
    """Error msg 'code' values for OFPET_QUEUE_OP_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: Specified table does not exist
    OFPTMFC_BAD_TABLE = 0,
    #: Specified config does not exist
    OFPTMFC_BAD_CONFIG = 1

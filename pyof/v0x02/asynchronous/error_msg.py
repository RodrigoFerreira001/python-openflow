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
    #: New - added in v0x02
    #: Error in instruction list
    OFPET_BAD_INSTRUCTION = 3
    #: New - added in v0x02
    #: Error in Match
    OFPET_BAD_MATCH = 4
    #: Problem in modifying Flow entry
    OFPET_FLOW_MOD_FAILED = 5
    #: New - added in v0x02
    #: Problem modifying group entry
    OFPET_GROUP_MOD_FAILED = 6
    #: Problem in modifying Port entry
    OFPET_PORT_MOD_FAILED = 7
    #: New - added in v0x02
    #: Problem in handling tables
    OFPET_TABLE_MOD_FAILED = 8
    #: Problem in modifying Queue entry
    OFPET_QUEUE_OP_FAILED = 9
    #: New - added in v0x02
    #: Switch config request failed
    OFPET_SWITCH_CONFIG_FAILED = 10


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


class FlowModFailedCode(Enum):
    """Error_msg 'code' values for OFPET_FLOW_MOD_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: New - added v0x02
    #: Unspecified error
    OFPFMFC_UNKNOWN = 0
    #: Flow not added because of full tables
    OFPFMFC_ALL_TABLES_FULL = 1
    #: New - added v0x02
    #: Table does not exist
    OFPFMFC_BAD_TABLE_ID = 2
    #: Attempted to add overlapping flow with CHECK_OVERLAP flag set
    OFPFMFC_OVERLAP = 3
    #: Permissions error
    OFPFMFC_EPERM = 4
    #: Flow not added because of non-zero idle/hard timeout
    OFPFMFC_BAD_EMERG_TIMEOUT = 5
    #: Unknown command
    OFPFMFC_BAD_COMMAND = 6
    #: Unsupported action list - cannot process in the order specified
    OFPFMFC_UNSUPPORTED = 7


class BadMatch(Enum):
    """Error_msg 'code' values for OFPET_BAD_MATCH.

    'data' contains at least the first 64 bytes of the failed request.
    """
    #: Unsupported match type specified by the match
    OFPBMC_BAD_TYPE = 0
    #: Lenght problem in match
    OFPBMC_BAD_LEN = 1
    #: Match uses an unsupported tag/encap
    OFPBMC_BAD_TAG = 2
    #: Unsupported datalink addr mask - switch does not support arbitrary datapath addr mask
    OFPBMC_BAD_DL_ADDR_MASK = 3
    #: Unsupported datalink addr mask - switch does not support arbitrary network addr mask
    OFPBMC_BAD_NW_ADDR_MASK = 4
    #: Unsupported wildcard specified in the match
    OFPBMC_BAD_WILDCARDS = 5
    #: Unsupported field in the match
    OFPBMC_BAD_FIELD = 6
    #: Unsupported field in the field
    OFPBMC_BAD_VALUE = 7


class BadInstruction(Enum):
    """Error_msg 'code' values for OFPET_BAD_INSTRUCTION.

    'data' contains at least the first 64 bytes of the failed request.
    """
    #: Unknown Instruction
    OFPBIC_UNKNOWN_INST = 0
    #: Switch or table does not support the instruction
    OFPBIC_UNSUP_INST = 1
    #: Invalid table-id specified
    OFPBIC_BAD_TABLE_ID = 2
    #: Metadata value unsupported by datapath
    OFPBIC_UNSUP_METADATA = 3
    #: Metadata mask value unsupported by datapath
    OFPBIC_UNSUP_METADATA_MASK = 4
    #: Specific experimenter instruction unsupported
    OFPBIC_UNSUP_EXP_INST = 5

class BadAction(Enum):

    #: Unknown action type
    OFPBAC_BAD_TYPE = 0
    #: Length problem in actions
    OFPBAC_BAD_LEN = 1
    #: New - Added in v0x02
    #: Unknow experimenter id specified
    OFPBAC_BAD_EXPERIMENTER = 2
    #: New - Added in v0x02
    #: Unknow action type for experimenter id
    OFPBAC_BAD_EXPERIMENTER_TYPE = 3
    #: Problem validating output action
    OFPBAC_BAD_OUT_PORT = 4
    #: Bad action argument
    OFPBAC_BAD_ARGUMENT = 5
    #: Permissions error
    OFPBAC_EPERM = 6
    #: Can’t handle this many actions
    OFPBAC_TOO_MANY = 7
    #: Problem validating output queue
    OFPBAC_BAD_QUEUE = 8
    #: New - Added in v0x02
    #: Invalid group id in forward action
    OFPBAC_BAD_OUT_GROUP = 9
    #: New - Added in v0x02
    #: Invalid group id in forward action
    OFPBAC_MATCH_INCONSISTENT = 10
    #: New - Added in v0x02
    #:  Action order is unsupported for the action list in an Apply-Actions instruction
    OFPBAC_UNSUPPORTED_ORDER = 11
    #: New - Added in v0x02
    #: Actions uses an unsupported tag/encap
    OFPBAC_BAD_TAG = 12


class BadRequestCode(Enum):
    """Error_msg 'code' values for OFPET_BAD_REQUEST.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: ofp_header.version not supported.
    OFPBRC_BAD_VERSION = 0
    #: ofp_header.type not supported.
    OFPBRC_BAD_TYPE = 1
    #: ofp_stats_request.type not supported.
    OFPBRC_BAD_STAT = 2
    #: Vendor not supported (in ofp_vendor_header or ofp_stats_request or
    #: ofp_stats_reply).
    OFPBRC_BAD_EXPERIMENTER = 3
    #: Vendor subtype not supported.
    OFPBRC_BAD_SUBTYPE = 4
    #: Permissions error.
    OFPBRC_EPERM = 5
    #: Wrong request length for type.
    OFPBRC_BAD_LEN = 6
    #: Specified buffer has already been used.
    OFPBRC_BUFFER_EMPTY = 7
    #: Specified buffer does not exist.
    OFPBRC_BUFFER_UNKNOWN = 8
    #: New - added to v0x02
    #: Specified table-id invalid or does not exist.
    OFPBRC_BAD_TABLE_ID = 9


class SwitchConfigFailed(Enum):
    """Error msg 'code' values for OFPET_SWITCH_CONFIG_FAILED.

    'data' contains at least the first 64 bytes of the failed request.
    """

    #: New - added in v0x02
    #: Specified flags is invalid
    OFPSCFC_BAD_FLAGS = 0
    #: New - added in v0x02
    #: Specified len is invalid
    OFPSCFC_BAD_LEN = 1

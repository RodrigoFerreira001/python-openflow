"""Defines Header classes and related items.

Only differences between versions.
"""
from enum import Enum, unique
from pyof.v0x01.common.header import Header as Header0x01
from pyof.v0x02.foundation.base import OFP_VERSION
from pyof.v0x02.foundation.basic_types import UBInt8


__all__ = ('Header', 'Type')


@unique
class Type(Enum):
    """Enumeration of Message Types."""

    # Symetric/Immutable messages
    OFPT_HELLO = 0
    OFPT_ERROR = 1
    OFPT_ECHO_REQUEST = 2
    OFPT_ECHO_REPLY = 3
    #: New - renamed in v0x02
    OFPT_EXPERIMENTER = 4

    # Switch configuration messages
    # Controller/Switch messages
    OFPT_FEATURES_REQUEST = 5
    OFPT_FEATURES_REPLY = 6
    OFPT_GET_CONFIG_REQUEST = 7
    OFPT_GET_CONFIG_REPLY = 8
    OFPT_SET_CONFIG = 9

    # Async messages
    OFPT_PACKET_IN = 10
    OFPT_FLOW_REMOVED = 11
    OFPT_PORT_STATUS = 12

    # Controller command messages
    # Controller/switch message
    OFPT_PACKET_OUT = 13
    OFPT_FLOW_MOD = 14
    OFPT_PORT_MOD = 15
    #: New - added in v0x02
    OFPT_TABLE_MOD = 16

    # Statistics messages
    # Controller/Switch message
    OFPT_STATS_REQUEST = 17
    OFPT_STATS_REPLY = 18

    # Barrier messages
    # Controller/Switch message
    OFPT_BARRIER_REQUEST = 19
    OFPT_BARRIER_REPLY = 20

    # Queue Configuration messages
    # Controller/Switch message
    OFPT_QUEUE_GET_CONFIG_REQUEST = 21
    OFPT_QUEUE_GET_CONFIG_REPLY = 22


class Header(Header0x01):
    """v0x02 Header differences."""

    version = UBInt8(OFP_VERSION)

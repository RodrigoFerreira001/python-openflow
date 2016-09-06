"""OFPT_GROUP_MOD message to modify the group table from the controller"""
from enum import Enum

# Local source tree imports
from pyof.v0x02.common.header import Header, Type
from pyof.v0x02.controller2switch.common import ListOfActions
from pyof.v0x02.foundation.base import GenericMessage, GenericStruct
from pyof.v0x02.foundation.basic_types import (FixedTypeList, PAD, UBInt8,
                                               UBInt16, UBInt32)

__all__ = ('Bucket', 'GroupMod', 'GroupModCommand', 'GroupType',
           'ListOfBuckets')

# Enums


class GroupModCommand(Enum):
    """Group commands to be used on GroupMod message"""
    #: New Group
    OFPGC_ADD = 0
    #: Modify all matching groups
    OFPGC_MODIFY = 1
    #: Delete all matching groups
    OFPGC_DELETE = 2


class GroupType(Enum):
    """Group types

    Values in the range [128, 255] are reserved for experimental use."""
    #: All (multicast/broadcast) group.
    OFPGT_ALL = 0
    #: Select group.
    OFPGT_SELECT = 1
    #: Indirect group.
    OFPGT_INDIRECT = 2
    #: Fast failover group.
    OFPGT_FF = 3


# Classes


class Bucket(GenericStruct):
    """Bucket for use in groups."""
    length = UBInt16()
    weight = UBInt16()
    watch_port = UBInt32()
    watch_group = UBInt32()
    pad = PAD(4)
    actions = ListOfActions()

    def __init__(self, length=None, weight=None, watch_port=None,
                 watch_group=None, actions=None):
        """The constructor just assings parameters to object attributes.

        Args:
            length (int): Length the bucket in bytes, including this header and
                any padding to make it 64-bit aligned.
            weight (int): Relative weight of bucket. Only defined for select
                groups.
            watch_port (int): Port whose state affects whether this bucket is
                live. Only required for fast failover groups.
            watch_group (int): Group whose state affects whether this bucket is
                live. Only required for fast failover groups.
            actions (ListOfActions): The action length is inferred from the
                length field in the header.
        """
        self.length = length
        self.weight = weight
        self.watch_port = watch_port
        self.watch_group = watch_group
        self.actions = [] if actions is None else actions


class ListOfBuckets(FixedTypeList):
    """List of buckets.

    Represented by instances of Bucket and used on GroupMod messages.
    """
    def __init__(self, items=None):
        """The constructor just assings parameters to object attributes.

        Args:
            items (Bucket): Instance or a list of instances.
        """
        super().__init__(pyof_class=Bucket, items=items)


class GroupMod(GenericMessage):
    """Group setup and teardown (controller -> datapath)."""
    header = Header(message_type=Type.OFPT_GROUP_MOD)
    command = UBInt16(enum_ref=GroupModCommand)
    group_type = UBInt8(enum_ref=GroupType)
    pad = PAD(1)
    group_id = UBInt32()
    buckets = ListOfBuckets()

    def __init__(self, xid=None, command=None, group_type=None, group_id=None,
                 buckets=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            command (GroupModCommand): One of OFPGC_*.
            group_type (GroupType): One of OFPGT_*.
            group_id (int): Group identifier.
            buckets (ListOfBuckets): The bucket length is inferred from the
                length field in the header.
        """
        super().__init__(xid)
        self.command = command
        self.group_type = group_type
        self.group_id = group_id
        self.buckets = [] if buckets is None else buckets

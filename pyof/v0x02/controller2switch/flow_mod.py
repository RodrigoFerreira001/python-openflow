"""Modifications to the flow table from the controller."""
# Local source tree imports
from pyof.v0x02.common.flow_match import Match
from pyof.v0x02.common.header import Header, Type
from pyof.v0x02.common.phy_port import Port
from pyof.v0x02.foundation.base import GenericBitMask, GenericMessage
from pyof.v0x02.foundation.basic_types import (PAD, UBInt8, UBInt16, UBInt32,
                                               UBInt64)

from pyof.v0x01.controller2switch.flow_mod import FlowModCommand

__all__ = ('FlowMod', 'FlowModCommand', 'FlowModFlags')

# Enums


class FlowModFlags(GenericBitMask):
    """Types to be used in Flags field."""

    #: Send flow removed message when flow expires or is deleted
    OFPFF_SEND_FLOW_REM = 1 << 0
    #: Check for overlapping entries first
    OFPFF_CHECK_OVERLAP = 1 << 1


# Classes


class FlowMod(GenericMessage):
    """Modifies the flow table from the controller."""

    header = Header(message_type=Type.OFPT_FLOW_MOD)
    cookie = UBInt64()
    cookie_mask = UBInt64()
    table_id = UBInt8()
    command = UBInt8(enum_ref=FlowModCommand)
    idle_timeout = UBInt16()
    hard_timeout = UBInt16()
    priority = UBInt16()
    buffer_id = UBInt32()
    out_port = UBInt32(enum_ref=Port)
    out_group = UBInt32()
    flags = UBInt16(enum_ref=FlowModFlags)
    pad = PAD(2)
    match = Match()
    instructions = ListOfInstructions()

    def __init__(self, xid=None, cookie=None, cookie_mask=None, table_id=None,
                 command=None, idle_timeout=None, hard_timeout=None,
                 priority=None, buffer_id=None, out_port=None, out_group=None,
                 flags=None, match=None, instructions=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            cookie (int): Opaque controller-issued identifier.
            cookie_mask (int): Mask used to restrict the cookie bits that must
                match when the command is OFPFC_MODIFY* or OFPFC_DELETE*.
                A value of 0 indicates no restriction.
            table_id (int): ID of the table to put the flow in.
            command (FlowModCommand): One of OFPFC_*.
            idle_timeout (int): Idle time before discarding (seconds).
            hard_timeout (int): Max time before discarding (seconds).
            priority (int): Priority level of flow entry.
            buffer_idle (int): Buffered packet to apply to (or -1).
                Not meaningful for OFPFC_DELETE*.
            out_port (Port): For OFPFC_DELETE* commands, require matching
                entries to include this as an output port.
                A value of OFPP_ANY indicates no restriction.
            out_group (): For OFPFC_DELETE* commands, require matching
                entries to include this as an output group.
                A value of OFPG_ANY indicates no restriction.
            flags (FlowModFlags): One of OFPFF_*.
            match (Match): Fields to match.
            instructions (ListOfInstructions): Instruction set.
        """
        super().__init__(xid)
        self.cookie = cookie
        self.cookie_mask = cookie_mask
        self.table_id = table_id
        self.command = command
        self.idle_timeout = idle_timeout
        self.hard_timeout = hard_timeout
        self.priority = priority
        self.buffer_id = buffer_id
        self.out_port = out_port
        self.out_group = out_group
        self.flags = flags
        self.match = match
        self.instructions = [] if instructions is None else instructions

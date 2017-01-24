"""Defines flow statistics structures and related items."""
from enum import Enum

from pyof.v0x01.common.flow_match import GenericBitMask
from pyof.v0x01.common.flow_match import Match as Match_v0x01

from pyof.foundation.basic_types import (HWAddress, IPAddress, Pad,
                                         UBInt8, UBInt16, UBInt32, UBInt64)

OFPMT_STANDARD_LENGTH = 88

class MatchType(Enum):
    """

    """
    # The match fields defined in the ofp_match structure apply
    OFPMT_STANDARD = 0

class FlowWildCards(GenericBitMask):
    """"""
    OFPFW_IN_PORT     = 1 << 0,  # Switch input port.
    OFPFW_DL_VLAN     = 1 << 1,  # VLAN id.
    OFPFW_DL_VLAN_PCP = 1 << 2,  # VLAN priority.
    OFPFW_DL_TYPE     = 1 << 3,  # Ethernet frame type.
    OFPFW_NW_TOS      = 1 << 4,  # IP ToS (DSCP field, 6 bits).
    OFPFW_NW_PROTO    = 1 << 5,  # IP protocol.
    OFPFW_TP_SRC      = 1 << 6,  # TCP/UDP/SCTP source port.
    OFPFW_TP_DST      = 1 << 7,  # TCP/UDP/SCTP destination port.
    OFPFW_MPLS_LABEL  = 1 << 8,  # MPLS label.
    OFPFW_MPLS_TC     = 1 << 9,  # MPLS TC.

    #: Wildcard all fields.
    OFPFW_ALL           = ((1 << 10) - 1)

class Match(Match_v0x01):
    match_type = UBInt16(value=MatchType.OFPMT_STANDARD, enum_ref=MatchType)
    length = UBInt16(OFPMT_STANDARD_LENGTH)
    in_port = UBInt16(0)
    wildcards = UBInt32(value=FlowWildCards.OFPFW_ALL, enum_ref=FlowWildCards)
    #: Ethernet source address. (default: '00:00:00:00:00:00')
    dl_src = HWAddress()
    #: Ethernet destination address. (default: '00:00:00:00:00:00')
    dl_src_mask = HWAddress()
    #: Ethernet source address. (default: '00:00:00:00:00:00')
    dl_dst = HWAddress()
    #: Ethernet destination address. (default: '00:00:00:00:00:00')
    dl_dst_mask = HWAddress()

    #: Input VLAN id. (default: 0)
    dl_vlan = UBInt16(0)
    #: Input VLAN priority. (default: 0)
    dl_vlan_pcp = UBInt8(0)
    #: Align to 64-bits.
    pad1 = Pad(1)
    dl_type = UBInt16(0)
    nw_tos = UBInt8(0)
    nw_proto = UBInt8(0)
    #: ARP opcode.
    nw_src = IPAddress()
    nw_src_mask = UBInt32()
    nw_dst = IPAddress()
    nw_dst_mask = UBInt32()
    tp_src = UBInt16()
    tp_dst = UBInt16()
    mpls_label = UBInt16()
    mpls_tc = UBInt8()
    #: Align to 64-bits.
    pad2 = Pad(3)
    metadata = UBInt64()
    metadata_mask = UBInt64()

class VlanId(Enum):
    """"""
    OFPVID_ANY  = 0xfffe
    OFPVID_NONE = 0xffff

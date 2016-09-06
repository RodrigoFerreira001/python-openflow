"""Defines flow statistics structures and related items."""
from enum import Enum

from pyof.v0x02.foundation.base import GenericBitMask, GenericStruct
from pyof.v0x02.foundation.basic_types import (PAD, HWAddress, UBInt8, UBInt16,
                                               UBInt32, UBInt64)

__all__ = ('OFPMT_STANDARD_LENGTH', 'FlowWildCards', 'Match', 'MatchType')


#: Length of :class:`.Match`.
OFPMT_STANDARD_LENGTH = 88


class MatchType(Enum):
    """Indicate the match structure is in use.

    The match type indicates the match structure (set of fields that compose
    the match) in use. The match type is placed in the type field at the
    beginning of all match structures. The "standard" type corresponds to
    ofp_match and must be supported by all OpenFlow switches. Extensions that
    define other match types may be published on the OpenFlow wiki. Support for
    extensions is optional.
    """

    #: The match fields defined in the ofp_match structure apply
    OFPMT_STANDARD = 0


class FlowWildCards(GenericBitMask):
    """Wildcards used to identify flows."""

    #: Switch input port.
    OFPFW_IN_PORT = 1 << 0
    #: VLAN id.
    OFPFW_DL_VLAN = 1 << 1
    #: VLAN priority.
    OFPFW_DL_VLAN_PCP = 1 << 2
    #: Ethernet frame type.
    OFPFW_DL_TYPE = 1 << 3
    #: IP ToS (DSCP field, 6 bits).
    OFPFW_NW_TOS = 1 << 4
    #: IP protocol.
    OFPFW_NW_PROTO = 1 << 5
    #: TCP/UDP/SCTP source port.
    OFPFW_TP_SRC = 1 << 6
    #: TCP/UDP/SCTP destination port.
    OFPFW_TP_DST = 1 << 7
    #: MPLS label.
    OFPFW_MPLS_LABEL = 1 << 8
    #: MPLS TC.
    OFPFW_MPLS_TC = 1 << 9

    #: Wildcard all fields.
    OFPFW_ALL = ((1 << 10) - 1)


class Match(GenericStruct):
    """Describes a flow entry. Fields to match against flows."""

    match_type = UBInt16(enum_ref=MatchType)
    length = UBInt16()
    in_port = UBInt32()
    wildcards = UBInt32(enum_ref=FlowWildCards)
    dl_src = HWAddress()
    dl_src_mask = HWAddress()
    dl_dst = HWAddress()
    dl_dst_mask = HWAddress()
    dl_vlan = UBInt16()
    dl_vlan_pcp = UBInt8()
    #: Align to 64-bits.
    pad1 = PAD(1)
    dl_type = UBInt16()
    nw_tos = UBInt8()
    nw_proto = UBInt8()

    nw_src = UBInt32()
    nw_src_mask = UBInt32()
    nw_dst = UBInt32()
    nw_dst_mask = UBInt32()
    tp_src = UBInt16()
    tp_dst = UBInt16()
    mpls_label = UBInt32()
    mpls_tc = UBInt8()
    #: Align to 64-bits.
    pad2 = PAD(3)
    metadata = UBInt64()
    metadata_mask = UBInt64()

    # disable too many local variables warning
    # pylint: disable=R0914
    def __init__(self, match_type=MatchType.OFPMT_STANDARD,
                 length=OFPMT_STANDARD_LENGTH, in_port=None, wildcards=None,
                 dl_src=None, dl_src_mask=None, dl_dst=None, dl_dst_mask=None,
                 dl_vlan=None, dl_vlan_pcp=None, dl_type=None, nw_tos=None,
                 nw_proto=None, nw_src=None, new_src_mask=None, nw_dst=None,
                 nw_dst_mask=None, tp_src=None, tp_dst=None, mpls_label=None,
                 mpls_tc=None, metadata=None, metadata_mask=None):
        """All the constructor parameters below are optional.

        Args:
            match_type (MatchType): One of OFPMT_*.
            length (int): Length of this struct. Defaults to 88.
            in_port (int): Input switch port.
            wildcards (FlowWildCards): Wildcards fields.
            dl_src (HWAddress): Ethernet source address.
            dl_src_mask (HWAddress): Ethernet source address mask.
            dl_dst (HWAddress): Ethernet destination address.
            dl_dst_mask (HWAddress): Ethernet destination address mask.
            dl_vlan (int): Input VLAN id.
            dl_vlan_pcp (int): Input VLAN priority.
            dl_type (int): Ethernet frame type.
            nw_tos (int): IP ToS (actually DSCP field, 6 bits).
            nw_proto (int): IP protocol or lower 8 bits of ARP opcode.
            nw_src (int): IP source address.
            nw_src_mask (int): IP source address mask.
            nw_dst (int): IP destination address.
            nw_dst_mask (int): IP destination address mask.
            tp_src (int): TCP/UDP source port.
            tp_dst (int): TCP/UDP destination port.
            mpls_label (int): MPLS label.
            mpls_tc (int): MPLS TC.
            metadata (int): Metadata passed between tables.
            metadata_mask (int): Mask for metadata.
        """
        super().__init__()
        self.wildcards = wildcards
        self.in_port = in_port
        self.dl_src = dl_src
        self.dl_dst = dl_dst
        self.dl_vlan = dl_vlan
        self.dl_vlan_pcp = dl_vlan_pcp
        self.dl_type = dl_type
        self.nw_tos = nw_tos
        self.nw_proto = nw_proto
        self.nw_src = nw_src
        self.nw_dst = nw_dst
        self.tp_src = tp_src
        self.tp_dst = tp_dst

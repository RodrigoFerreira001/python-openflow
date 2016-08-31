"""Defines physical port classes and related items."""
from enum import Enum, unique

from pyof.v0x01.foundation.base import (GenericBitMask, GenericStruct,
                                        OFP_MAX_PORT_NAME_LEN)
from pyof.v0x01.foundation.basic_types import UBInt32, HWAddress, Char, PAD


@unique
class PortNo(Enum):
    """Port numbering. Ports are numbered starting from 1."""

    #: Maximum number of physical switch ports.
    OFPP_MAX = 0xffffff00
    # Fake output "ports".
    #: Send the packet out the input port. This virtual port must be explicitly
    #: used in order to send back out of the input port.
    OFPP_IN_PORT = 0xfffffff8
    #: Submit the packet to the first flow table NB: This destination port can
    #: only be used in packet-out messages.
    OFPP_TABLE = 0xfffffff9
    #: Process with normal L2/L3 switching.
    OFPP_NORMAL = 0xfffffffa
    #: All physical ports in VLAN, except input
    #: port and those blocked or link down.
    OFPP_FLOOD = 0xfffffffb
    #: All physical ports except input port.
    OFPP_ALL = 0xfffffffc
    #: Send to controller.
    OFPP_CONTROLLER = 0xfffffffd
    #: Local openflow "port".
    OFPP_LOCAL = 0xfffffffe
    #: Wildcard port used only for flow mod (delete) and flow stats requests.
    #: Selects all flows regardless of output port (including flows with no
    #: output port).
    OFPP_ANY = 0xffffffff


class PortConfig(GenericBitMask):
    """Flags to indicate behavior of the physical port.

    These flags are used in :class:`.Port` to describe the current
    configuration. They are used in the :class:`.PortMod` message to configure
    the port's behavior.
    """

    #: Port is administratively down.
    OFPPC_PORT_DOWN = 1 << 0
    #: Drop all packets received by port.
    OFPPC_NO_RECV = 1 << 2
    #: Drop packets forwarded to port.
    OFPPC_NO_FWD = 1 << 5
    #: Do not send packet-in msgs for port.
    OFPPC_NO_PACKET_IN = 1 << 6


class PortFeatures(GenericBitMask):
    """Features of ports available in a datapath."""

    #: 10 Mb half-duplex rate support.
    OFPPF_10MB_HD = 1 << 0
    #: 10 Mb full-duplex rate support.
    OFPPF_10MB_FD = 1 << 1
    #: 100 Mb half-duplex rate support.
    OFPPF_100MB_HD = 1 << 2
    #: 100 Mb full-duplex rate support.
    OFPPF_100MB_FD = 1 << 3
    #: 1 Gb half-duplex rate support.
    OFPPF_1GB_HD = 1 << 4
    #: 1 Gb full-duplex rate support.
    OFPPF_1GB_FD = 1 << 5
    #: 10 Gb full-duplex rate support.
    OFPPF_10GB_FD = 1 << 6
    #: 40 Gb full-duplex rate support.
    OFPPF_40GB_FD = 1 << 7
    #: 100 Gb full-duplex rate support.
    OFPPF_100GB_FD = 1 << 8
    #: 1 Tb full-duplex rate support.
    OFPPF_1TB_FD = 1 << 9
    #: Other rate, not in the list.
    OFPPF_OTHER = 1 << 10
    #: Copper medium.
    OFPPF_COPPER = 1 << 11
    #: Fiber medium.
    OFPPF_FIBER = 1 << 12
    #: Auto-negotiation.
    OFPPF_AUTONEG = 1 << 13
    #: Pause.
    OFPPF_PAUSE = 1 << 14
    #: Asymmetric pause.
    OFPPF_PAUSE_ASYM = 1 << 15


class PortState(GenericBitMask):
    """Current state of the physical port.

    These are not configurable from the controller.

    The ``OFPPS_STP_*`` bits have no effect on switch operation. The controller
    must adjust :attr:`PortConfig.OFPPC_NO_RECV`,
    :attr:`~PortConfig.OFPPC_NO_FWD`, and
    :attr:`~PortConfig.OFPPC_NO_PACKET_IN` appropriately to fully implement an
    802.1D spanning tree.
    """

    #: No physical link present.
    OFPPS_LINK_DOWN = 1 << 0
    #: Port is blocked
    OFPPS_BLOCKED = 1 << 1
    #: Live for Fast Failover Group.
    OFPPS_LIVE = 1 << 2


class Port(GenericStruct):
    """Description of a port.

    The port_no field is a value the datapath associates with a physical port.
    The hw_addr field typically is the MAC address for the port;
    :data:`.OFP_ETH_ALEN` is 6. The name field is a
    null-terminated string containing a human-readable name for the interface.
    The value of :data:`.OFP_MAX_PORT_NAME_LEN` is 16.

    :attr:`curr`, :attr:`advertised`, :attr:`supported` and :attr:`peer` are
    bitmaps of :class:`PortFeatures` enum values that describe features. If
    unsupported or unavailable, set all bits to zero.
    """

    port_no = UBInt32()
    pad = PAD(4)
    hw_addr = HWAddress()
    pad2 = PAD(2)
    name = Char(length=OFP_MAX_PORT_NAME_LEN)

    config = UBInt32(enum_ref=PortConfig)
    state = UBInt32(enum_ref=PortState)

    curr = UBInt32(enum_ref=PortFeatures)
    advertised = UBInt32(enum_ref=PortFeatures)
    supported = UBInt32(enum_ref=PortFeatures)
    peer = UBInt32(enum_ref=PortFeatures)

    curr_speed = UBInt32()
    max_speed = UBInt32()

    def __init__(self, port_no=None, hw_addr=None, name=None, config=None,
                 state=None, curr=None, advertised=None, supported=None,
                 peer=None, curr_speed=None, max_speed=None):
        """The constructor takes the optional parameters below.

        Args:
            port_no (int): Port number.
            hw_addr (HWAddress): Hardware address.
            name(str): Null-terminated name.
            config (PortConfig): Bitmap of OFPPC* flags.
            state (PortState): Bitmap of OFPPS* flags.
            curr (PortFeatures): Current features.
            advertised (PortFeatures): Features being advertised by the port.
            supported (PortFeatures): Features supported by the port.
            peer (PortFeatures): Features advertised by peer.
            curr_speed (int): Current port bitrate in kbps.
            max_speed (int): Max port bitrate in kbps.
        """
        super().__init__()
        self.port_no = port_no
        self.hw_addr = hw_addr
        self.name = name
        self.config = config
        self.state = state
        self.curr = curr
        self.advertised = advertised
        self.supported = supported
        self.peer = peer
        self.curr_speed = curr_speed
        self.max_speed = max_speed

"""Defines Features Reply classes and related items."""
# Local source tree imports
from pyof.v0x02.common.header import Header, Type
from pyof.v0x02.common.port import ListOfPorts
from pyof.v0x02.foundation.base import GenericBitMask, GenericMessage
from pyof.v0x02.foundation.basic_types import PAD, UBInt8, UBInt32, UBInt64

__all__ = ('FeaturesReply', 'Capabilities', 'SwitchFeatures')


class Capabilities(GenericBitMask):
    """Capabilities supported by the datapath."""

    #: Flow statistics
    OFPC_FLOW_STATS = 1 << 0
    #: Table statistics
    OFPC_TABLE_STATS = 1 << 1
    #: Port statistics
    OFPC_PORT_STATS = 1 << 2
    #: Group statistics
    OFPC_GROUP_STATS = 1 << 3
    #: Can reassembe IP fragments
    OFPC_IP_REASM = 1 << 5
    #: Queue statistics
    OFPC_QUEUE_STATS = 1 << 6
    #: Match IP addresses in ARP pkts
    OFPC_ARP_MATCH_IP = 1 << 7


# Classes


class SwitchFeatures(GenericMessage):
    """Message sent by the switch device to the controller.

    This message is the response for a features_request message, sent by the
    controller to the switch device. The 'OFPT_FEATURES_REPLY' message inherits
    from this class, despite the strange name.
    """

    header = Header(message_type=Type.OFPT_FEATURES_REPLY)
    datapath_id = UBInt64()
    n_buffers = UBInt32()
    n_tables = UBInt8()
    #: Align to 64-bits.
    pad = PAD(3)
    # Features
    capabilities = UBInt32(enum_ref=Capabilities)
    reserved = UBInt32()
    ports = ListOfPorts()

    def __init__(self, xid=None, datapath_id=None, n_buffers=None,
                 n_tables=None, capabilities=None, ports=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            datapath_id (int): UBInt64 datapath unique ID.
                The lower 48-bits are for MAC address, while
                the upper 16-bits are implementer-defined.
            n_buffers (int): UBInt32 max packets buffered at once.
            n_tables (int): UBInt8 number of tables supported by datapath.
            capabilities (int): UBInt32 bitmap of supported capabilities.
            ports (int): Port definitions.
        """
        super().__init__(xid)
        self.datapath_id = datapath_id
        self.n_buffers = n_buffers
        self.n_tables = n_tables
        self.capabilities = capabilities
        self.ports = [] if ports is None else ports


class FeaturesReply(SwitchFeatures):
    """'OFPT_FEATURES_REPLY' message."""

    def __init__(self, xid=None, datapath_id=None, n_buffers=None,
                 n_tables=None, capabilities=None, ports=None):
        """The constructor just assings parameters to object attributes.

        Args:
            xid (int): xid to be used on the message header.
            datapath_id (int): UBInt64 datapath unique ID.
                The lower 48-bits are for MAC address, while
                the upper 16-bits are implementer-defined.
            n_buffers (int): UBInt32 max packets buffered at once.
            n_tables (int): UBInt8 number of tables supported by datapath.
            capabilities (int): UBInt32 bitmap of supported capabilities.
            ports (int): Port definitions.
        """
        self.__ordered__ = super().__ordered__  # pylint: disable=no-member
        super().__init__(xid, datapath_id, n_buffers, n_tables, capabilities,
                         ports)
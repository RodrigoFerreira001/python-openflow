"""Defines OpenFlow queues structures and related items."""

# System imports
import enum

# Local source tree imports
from pyof.v0x01.foundation import base, basic_types


# Third-party imports


__all__ = ('QueuePropHeader', 'PacketQueue', 'QueuePropMinRate',
           'QueueProperties', 'ListOfProperties', 'ListOfQueues')

# Enums


class QueueProperties(enum.Enum):
    """Describe queue properties."""

    #: No property defined for queue (default)
    OFPQT_NONE = 0
    #: Minimum datarate guaranteed
    OFPQT_MIN_RATE = 1


# Classes


class ListOfProperties(basic_types.FixedTypeList):
    """List of properties.

    Represented by instances of :class:`QueuePropHeader` and used on
    :class:`PacketQueue` objects.
    """

    def __init__(self, items=None):
        """The contructor takes the paremeters below.

        Args:
            items (:class:`list` of/or :class:`QueuePropHeader`):
                :class:`QueuePropHeader` instance or list of instances.
        """
        super().__init__(pyof_class=QueuePropHeader,
                         items=items)


class QueuePropHeader(base.GenericStruct):
    """Describe the header of each queue property."""

    property = basic_types.UBInt16(enum_ref=QueueProperties)
    len = basic_types.UBInt16()
    #: 64-bit alignment
    pad = basic_types.PAD(4)

    def __init__(self, prop=None, length=None):
        """The contructor takes the paremeters below.

        Args:
            property (QueueProperties): The queue property.
            len (int): Length of property, including this header.
        """
        super().__init__()
        self.property = prop
        self.len = length


class PacketQueue(base.GenericStruct):
    """Describe a queue."""

    queue_id = basic_types.UBInt32()
    length = basic_types.UBInt16()
    #: 64-bit alignment.
    pad = basic_types.PAD(2)
    properties = ListOfProperties()

    def __init__(self, queue_id=None, length=None, properties=None):
        """The contructor takes the paremeters below.

        Args:
            queue_id (int): ID of the specific queue.
            length (int): Length in bytes of this queue desc.
            properties(ListOfProperties): Queue's list of properties. Default
                is an empty list.
        """
        super().__init__()
        self.queue_id = queue_id
        self.length = length
        self.properties = [] if properties is None else properties


class QueuePropMinRate(base.GenericStruct):
    """Define the minimum-rate type queue."""

    prop_header = QueuePropHeader(prop=QueueProperties.OFPQT_MIN_RATE,
                                  length=16)
    rate = basic_types.UBInt16()
    #: 64-bit alignmet.
    pad = basic_types.PAD(6)

    def __init__(self, rate=None):
        """The contructor takes the paremeters below.

        Args:
            rate (int): In 1/10 of a percent (1000 -> 100%); >1000 -> disabled.
        """
        super().__init__()
        self.rate = rate


class ListOfQueues(basic_types.FixedTypeList):
    """List of queues.

    Represented by instances of :class:`PacketQueue` and used on
    :class:`QueueGetConfigReply` objects.
    """

    def __init__(self, items=None):
        """The contructor takes the paremeters below.

        Args:
            items (:class:`list` of/or :class:`PacketQueue`):
                :class:`PacketQueue` instance or list of instances.
        """
        super().__init__(pyof_class=PacketQueue,
                         items=items)

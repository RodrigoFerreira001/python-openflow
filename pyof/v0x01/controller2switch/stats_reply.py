"""Response the stat request packet from the controller."""
from pyof.foundation.base import GenericMessage
from pyof.foundation.basic_types import BinaryData, FixedTypeList, UBInt16
from pyof.v0x01.common.header import Header, Type
from pyof.v0x01.controller2switch.common import (AggregateStatsReply,
                                                 DescStats, FlowStats,
                                                 PortStats, QueueStats,
                                                 StatsTypes, TableStats)

__all__ = ('StatsReply',)


class StatsReply(GenericMessage):
    """Class implements the response to the stats request."""

    #: OpenFlow :class:`.Header`
    header = Header(message_type=Type.OFPT_STATS_REPLY)
    body_type = UBInt16(enum_ref=StatsTypes)
    flags = UBInt16()
    body = BinaryData()

    # List of Class that can be packed/unpacked using StatsReply
    _types = [DescStats, FlowStats, AggregateStatsReply, TableStats,
              PortStats, QueueStats]

    def __init__(self, xid=None, body_type=None, flags=None, body=b''):
        """The constructor just assings parameters to object attributes.

        Args:
            body_type (StatsTypes): One of the OFPST_* constants.
            flags (int): OFPSF_REQ_* flags (none yet defined).
            body (BinaryData): Body of the request.
        """
        super().__init__(xid)
        self.body_type = body_type
        self.flags = flags
        self.body = body

    def pack(self):
        """Pack a StatsReply using the object's attributes.

        This method will pack the attribute body and body_type before pack the
        StatsReply object, then will return this struct as a binary data.

        Returns:
            stats_reply_packed (bytes): Binary data with StatsReply packed.
        """
        buff = self.body

        if self.body and hasattr(self.body, 'pack'):
            self.body = BinaryData(buff.pack())
        stats_reply_packed = super().pack()
        self.body = buff

        return stats_reply_packed

    def unpack(self, buff):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        This class' unpack method is like the :meth:`.GenericMessage.unpack`
        one, except for the ``body`` attribute which has its type determined
        by the ``body_type`` attribute.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
        """
        super().unpack(buff)
        self._unpack_body()

    def _unpack_body(self):
        """Unpack `body` replace it by the result."""
        obj = self._get_body_instance()
        obj.unpack(self.body.value)
        self.body = obj

    def _get_body_instance(self):
        """Method used to return the body instance."""
        if self.body_type.value == 0:
            return self._types[0]()
        elif self.body_type.value < len(self._types):
            return FixedTypeList(pyof_class=self._types[self.body_type.value])
        return BinaryData(b'')

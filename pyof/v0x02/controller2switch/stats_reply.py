"""Response the stat request packet from the controller."""
from pyof.foundation.basic_types import BinaryData, UBInt16, Pad
from pyof.v0x02.common.header import Header, Type

from pyof.v0x01.controller2switch.stats_reply import StatsReply
from pyof.v0x02.controller2switch.common import StatsTypes

StatsReply_v0x01  = StatsReply

__all__ = ('StatsReply',)


class StatsReply(StatsReply_v0x01):
    header = Header(message_type=Type.OFPT_STATS_REPLY)
    body_type = UBInt16(enum_ref=StatsTypes)
    flags =UBInt16()
    pad1 = Pad(4)
    body = BinaryData()

    _removed_attributes = ['body']

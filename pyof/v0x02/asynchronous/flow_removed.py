# System imports
from enum import Enum

from pyof.v0x01.asynchronous.flow_removed import FlowRemoved

__all__ = ('FlowRemoved', 'FlowRemovedReason')

# Enums


class FlowRemovedReason(Enum):
    """Why the flow was removed."""

    #: Flow idle time exceeded idle_timeout
    OFPRR_IDLE_TIMEOUT = 0
    #: Time exceeded hard_timeout
    OFPRR_HARD_TIMEOUT = 1
    #: Evicted by a DELETE flow mod
    OFPRR_DELETE = 2
    #: New - added in v0x02
    #: Group was removed
    OFPRR_GROUP_DELETE = 3

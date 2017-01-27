"""Defines Hello message."""

# System imports

# Third-party imports

from pyof.foundation.base import GenericMessage
from pyof.v0x01.common.header import Header, Type

__all__ = ('Hello',)

# Classes


class Hello(GenericMessage, message_type='OFPT_HELLO'):
    """OpenFlow Hello Message.

    This message does not contain a body beyond the OpenFlow Header.
    """

    header = Header()

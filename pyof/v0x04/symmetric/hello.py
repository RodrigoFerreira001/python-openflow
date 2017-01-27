"""Defines Hello message."""

# System imports

# Third-party imports

from pyof.v0x01.symmetric.hello import Hello as _Hello
__all__ = ['Hello']

# Classes


class Hello(_Hello, message_type='OFPT_HELLO'):
    pass

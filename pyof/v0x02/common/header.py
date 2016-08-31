"""Defines Header classes and related items.

Only differences between versions.
"""
from pyof.v0x01.common.header import Header as Header0x01, Type
from pyof.v0x02.foundation.base import OFP_VERSION
from pyof.v0x02.foundation.basic_types import UBInt8


__all__ = ('Header', 'Type')


class Header(Header0x01):
    """v0x02 Header differences."""

    version = UBInt8(OFP_VERSION)

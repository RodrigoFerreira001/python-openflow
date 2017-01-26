"""General constants from python-openflow library."""

from enum import Enum

# Max values of each basic type
UBINT8_MAX_VALUE = 255
UBINT16_MAX_VALUE = 65535
UBINT32_MAX_VALUE = 4294967295
UBINT64_MAX_VALUE = 18446744073709551615

OFP_ETH_ALEN = 6
OFP_MAX_PORT_NAME_LEN = 16
OFP_MAX_TABLE_NAME_LEN = 32
SERIAL_NUM_LEN = 32
DESC_STR_LEN = 256


class PyofVersion(Enum):
    """Enumeration of openflow versions implemented (available) on the lib."""

    v0x01 = 0x01
    # v0x02 = 0x02
    # v0x03 = 0x03
    v0x04 = 0x04

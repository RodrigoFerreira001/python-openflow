"""Header testing."""
import unittest

from pyof.v0x02.common.header import Header


class TestHeader(unittest.TestCase):
    """Test Header changes between v0x01 and v0x02."""

    def test_version(self):
        """Version must be 0x02 for OF 1.1.0."""
        header = Header()
        self.assertEqual(0x02, header.version)

"""v0x02 Port tests."""
import unittest

from pyof.v0x02.common.port import Port


class TestPort(unittest.TestCase):
    """Test port differences in v0x02."""

    def test_minimum_size(self):
        """Size changed to 64 in v0x02."""
        self.assertEqual(64, Port().get_size())

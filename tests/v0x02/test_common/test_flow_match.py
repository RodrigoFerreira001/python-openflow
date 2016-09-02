"""Flow match tests."""
import unittest

from pyof.v0x02.common.flow_match import OFPMT_STANDARD_LENGTH, Match


class TestFlowMatch(unittest.TestCase):
    """Test v0x02 flow_match."""

    def test_size(self):
        """Test minimum Match size."""
        self.assertEqual(OFPMT_STANDARD_LENGTH, Match().get_size())

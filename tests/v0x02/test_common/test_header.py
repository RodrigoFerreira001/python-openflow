"""Testing Header structure."""
import os
import unittest
from unittest.mock import patch

from pyof.v0x02.common.header import Header, Type

class TestHeader(unittest.TestCase):
    """Test the message Header."""
    def setUp(self):
        """Setup Header_V0x02 with Hello Header."""
        self.message = Header()
        self.message.version = 2
        self.message.message_type = Type.OFPT_EXPERIMENTER
        self.message.length = 8
        self.message.xid = 1

    def test_size(self):
        self.assertEqual(self.message.get_size(), 8)

    def test_version(self):
        self.assertEqual(self.message.version, 2)

    def test_unpack(self):
        packed=  b'\x02\x04\x00\x08\x00\x00\x00\x01'
        unpacked = Header()
        unpacked.unpack(packed)
        self.assertEqual(unpacked, self.message)

    def test_pack(self):
        packed = b'\x02\x04\x00\x08\x00\x00\x00\x01'
        self.assertEqual(self.message.pack(), packed)

    @patch('pyof.v0x01.common.header.randint')
    def test_random_xid(self, m):
        Header(), Header()
        self.assertEqual(m.call_count, 2)

import unittest
import os

from pyof.v0x01.asynchronous import packet_in
from pyof.v0x01.common import header as of_header


class TestPacketIn(unittest.TestCase):
    """Test the PacketIn message"""

    def setUp(self):
        """Setup the TestPacketIn Class instantiating a PacketIn message"""
        self.message = packet_in.PacketIn()
        self.message.header.xid = 1
        self.message.buffer_id = 1
        self.message.total_len = 1
        self.message.in_port = 1
        self.message.reason = packet_in.PacketInReason.OFPR_ACTION

        self.head = of_header.Header()

    def test_size(self):
        """[Asynchronous/PacketIn] - size 18

        Different from the specification, the minimum size of this class is 18,
        not 20."""
        self.assertEqual(self.message.get_size(), 18)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Asynchronous/PacketIn] - packing"""
        # TODO
        pass

    def test_unpack(self):
        """[Asynchronous/PacketIn] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_packet_in.dat')


        total_len = 42
        in_port = 1
        reason = 0
        binaryData = b'\x00\x00\x01\x00\x00*\x00\x01\x00\x00\xff\xff\xff\xff\
\xff\xffJ\xae\x04\xe3p\xe8\x08\x06\x00\x01\x08\x00\x06\x04\x00\x01J\xae\x04\
\xe3p\xe8\n\x00\x00\x01\x00\x00\x00\x00\x00\x00\n\x00\x00\x02'

        with open(filename,'rb') as f:
            self.head.unpack(f.read(8))
            self.assertEqual(self.message.unpack(f.read()), None)

        self.assertEqual(self.message.total_len._value, total_len)
        self.assertEqual(self.message.in_port._value, in_port)
        self.assertEqual(self.message.reason._value, reason)
        self.assertEqual(self.message.data._value, binaryData)

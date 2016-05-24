import unittest
import os

from pyof.v0x01.common import flow_match
from pyof.v0x01.common import phy_port
from pyof.v0x01.controller2switch import flow_mod
from pyof.v0x01.common import header as of_header


class TestFlowMod(unittest.TestCase):

    def setUp(self):
        self.head = of_header.Header()

        self.message = flow_mod.FlowMod()
        self.message.header.xid = 1
        self.message.command = flow_mod.FlowModCommand.OFPFC_ADD
        self.message.match = flow_match.Match()
        self.message.cookie = 0
        self.message.idle_timeout = 300
        self.message.hard_timeout = 6000
        self.message.priority = 1
        self.message.buffer_id = 1
        self.message.out_port = phy_port.Port.OFPP_NONE
        self.message.flags = flow_mod.FlowModFlags.OFPFF_EMERG
        self.message.match.in_port = 80
        self.message.match.dl_src = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_dst = [1, 2, 3, 4, 5, 6]
        self.message.match.dl_vlan = 1
        self.message.match.dl_vlan_pcp = 1
        self.message.match.dl_type = 1
        self.message.match.nw_tos = 1
        self.message.match.nw_proto = 1
        self.message.match.nw_src = 10000
        self.message.match.nw_dst = 10000
        self.message.match.tp_src = 80
        self.message.match.tp_dst = 80

    def test_get_size(self):
        """[Controller2Switch/FlowMod] - size 72"""
        self.assertEqual(self.message.get_size(), 72)

    @unittest.skip('Not yet implemented')
    def test_pack(self):
        """[Controller2Switch/FlowMod] - packing"""
        # TODO
        pass

    def test_unpack_add(self):
        """[Controller2Switch/FlowMod] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_flow_add.dat')

        idle_timeout = 0
        hard_timeout = 0
        priority = 65000
        out_port = 65535
        flags = 0
        dl_src = (0, 0, 0, 0, 0, 0)
        dl_dst = (1, 35, 32, 0, 0, 1)

        with open(filename,'rb') as f:
            self.head.unpack(f.read(8))
            self.assertEqual(self.message.unpack(f.read()), None)

        self.assertEqual(self.message.command._value,
                         flow_mod.FlowModCommand.OFPFC_ADD.value)

        self.assertEqual(self.message.command._value,
                         flow_mod.FlowModCommand.OFPFC_ADD.value)

        self.assertEqual(self.message.idle_timeout._value,
                         idle_timeout)

        self.assertEqual(self.message.hard_timeout._value,
                         hard_timeout)

        self.assertEqual(self.message.priority._value,
                         priority)

        self.assertEqual(self.message.out_port._value,
                         out_port)

        self.assertEqual(self.message.flags._value,
                         flags)

        self.assertEqual(self.message.match.dl_src._value,
                         dl_src)

        self.assertEqual(self.message.match.dl_dst._value,
                         dl_dst)

    def test_unpack_delete(self):
        """[Controller2Switch/FlowMod] - unpacking"""
        filename = os.path.join(os.path.dirname(os.path.realpath('__file__')),
                                'raw/v0x01/ofpt_flow_delete.dat')
        idle_timeout = 0
        hard_timeout = 0
        priority = 32768
        out_port = 65535
        flags = 0
        dl_src = (0, 0, 0, 0, 0, 0)
        dl_dst = (0, 0, 0, 0, 0, 0)

        with open(filename,'rb') as f:
            self.head.unpack(f.read(8))
            self.assertEqual(self.message.unpack(f.read()), None)

        self.assertEqual(self.message.command._value,
                         flow_mod.FlowModCommand.OFPFC_DELETE.value)

        self.assertEqual(self.message.idle_timeout._value,
                         idle_timeout)

        self.assertEqual(self.message.hard_timeout._value,
                         hard_timeout)

        self.assertEqual(self.message.priority._value,
                         priority)

        self.assertEqual(self.message.out_port._value,
                         out_port)

        self.assertEqual(self.message.flags._value,
                         flags)

        self.assertEqual(self.message.command._value,
                         flow_mod.FlowModCommand.OFPFC_DELETE.value)

        self.assertEqual(self.message.match.dl_src._value,
                         dl_src)

        self.assertEqual(self.message.match.dl_dst._value,
                         dl_dst)

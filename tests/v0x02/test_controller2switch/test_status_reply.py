"""Testing StatusReply class."""
from pyof.v0x02.controller2switch.common import StatsTypes
from pyof.v0x02.controller2switch.stats_reply import StatsReply

from tests.test_struct import TestStruct


class TestStatsReply(TestStruct):
    """Test for StatsReply message."""

    @classmethod
    def setUpClass(cls):
        """[Controller2Switch/StatsReply] - size 12."""
        super().setUpClass()
        super().set_raw_dump_file('v0x02', 'ofpt_stats_reply')
        super().set_raw_dump_object(StatsReply, xid=1,
                                    body_type=StatsTypes.OFPST_GROUP,
                                    flags=0x0001, body=[])
        super().set_minimum_size(16)

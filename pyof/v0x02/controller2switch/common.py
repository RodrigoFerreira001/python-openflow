from enum import Enum

class StatsTypes(Enum):
    OFPST_DESC = 0,
    OFPST_FLOW = 1
    OFPST_AGGREGATE = 2
    OFPST_TABLE = 3
    OFPST_PORT = 5
    OFPST_QUEUE = 6
    OFPST_GROUP = 7
    OFPST_GROUP_DESC = 8
    OFPST_EXPERIMENTER = 0xffff


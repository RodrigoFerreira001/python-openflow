"""Defines common structures and enums for controller2switch."""
from pyof.v0x01.controller2switch.common import (aggregatestatsreply,
                                                 aggregatestatsrequest,
                                                 configflags, descstats,
                                                 flowstats, flowstatsrequest,
                                                 listofactions, portstats,
                                                 portstatsrequest, queuestats,
                                                 queuestatsrequest, statstypes,
                                                 switchconfig, tablestats)

__all__ = ('aggregatestatsreply', 'aggregatestatsrequest', 'configflags',
           'descstats', 'flowstats', 'flowstatsrequest', 'listofactions',
           'portstats', 'portstatsrequest', 'queuestats', 'queuestatsrequest',
           'statstypes', 'switchconfig', 'tablestats')

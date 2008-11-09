# XIVO Daemon

__version__   = '$Revision$'
__date__      = '$Date$'
__copyright__ = 'Copyright (C) 2007, 2008, Proformatique'
__author__    = 'Corentin Le Gall'

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Alternatively, XIVO Daemon is available under other licenses directly
# contracted with Pro-formatique SARL. See the LICENSE file at top of the
# source tree or delivered in the installable package in which XIVO Daemon
# is distributed for more details.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, you will find one at
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>.

import logging
from xivo_ctiservers.cti_anylist import AnyList

log = logging.getLogger('phonelist')

class PhoneList(AnyList):
        def __init__(self, newurls = []):
                self.anylist_properties = { 'keywords' : [],
                                            'name' : 'phones',
                                            'action' : 'getphoneslist',
                                            'urloptions' : (1, 12, False) }
                AnyList.__init__(self, newurls)
                return
        
        def ami_dial(self, phoneidsrc, phoneiddst, uidsrc, uiddst, puidsrc, puiddst):
                if phoneidsrc in self.keeplist:
                        if uidsrc in self.keeplist[phoneidsrc]['comms']:
                                pass
                        else:
                                infos = {'thischannel' : puidsrc.get('channel'),
                                         'peerchannel' : puidsrc.get('dial'),
                                         'status' : 'calling',
                                         'time-dial' : puidsrc.get('time-dial'),
                                         'calleridname' : puidsrc.get('calleridname'),
                                         'calleridnum' : puidsrc.get('calleridnum')
                                         }
                                self.keeplist[phoneidsrc]['comms'][uidsrc] = infos
                if phoneiddst in self.keeplist:
                        if uiddst in self.keeplist[phoneiddst]['comms']:
                                pass
                        else:
                                infos = {'thischannel' : puiddst.get('channel'),
                                         'peerchannel' : puiddst.get('dial'),
                                         'status' : 'ringing',
                                         'time-dial' : puiddst.get('time-dial'),
                                         'calleridname' : puidsrc.get('calleridname'),
                                         'calleridnum' : puidsrc.get('calleridnum')
                                         }
                                self.keeplist[phoneiddst]['comms'][uiddst] = infos
                return
        
        def ami_link(self, phoneidsrc, phoneiddst, uidsrc, uiddst, puidsrc, puiddst):
                if phoneidsrc in self.keeplist:
                        if uidsrc in self.keeplist[phoneidsrc]['comms']:
                                pass
                        else:
                                self.keeplist[phoneidsrc]['comms'][uidsrc] = puidsrc
                if phoneiddst in self.keeplist:
                        if uiddst in self.keeplist[phoneiddst]['comms']:
                                pass
                        else:
                                self.keeplist[phoneiddst]['comms'][uiddst] = puiddst
                return
        
        def ami_unlink(self, phoneidsrc, phoneiddst, uidsrc, uiddst, puidsrc, puiddst):
                if phoneidsrc in self.keeplist:
                        if uidsrc in self.keeplist[phoneidsrc]['comms']:
                                pass
                        else:
                                self.keeplist[phoneidsrc]['comms'][uidsrc] = puidsrc
                if phoneiddst in self.keeplist:
                        if uiddst in self.keeplist[phoneiddst]['comms']:
                                pass
                        else:
                                self.keeplist[phoneiddst]['comms'][uiddst] = puiddst
                return
        
        def ami_hangup(self, phoneid, uid):
                if phoneid in self.keeplist and uid in self.keeplist[phoneid]['comms']:
                        self.keeplist[phoneid]['comms'][uid]['status'] = 'hangup'
                return
        
        def clear(self, phoneid, uid):
                if phoneid in self.keeplist and uid in self.keeplist[phoneid]['comms']:
                        del self.keeplist[phoneid]['comms'][uid]
                return
        
        def status(self, phoneid):
                tosend = {}
                if phoneid in self.keeplist:
                        tosend = { 'class' : 'phones',
                                   'direction' : 'client',
                                   'function' : 'update',
                                   'phoneid' : phoneid,
                                   'status' : self.keeplist[phoneid] }
                return tosend
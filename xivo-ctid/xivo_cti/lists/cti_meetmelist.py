# XiVO CTI Server

# Copyright (C) 2007-2011  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Alternatively, XiVO CTI Server is available under other licenses directly
# contracted with Pro-formatique SARL. See the LICENSE file at top of the
# source tree or delivered in the installable package in which XiVO CTI Server
# is distributed for more details.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from xivo_cti.cti_anylist import AnyList

import logging
from xivo_cti.cti.commands.invite_confroom import InviteConfroom

logger = logging.getLogger('meetmelist')


class MeetmeList(AnyList):

    def __init__(self, newurls=[], useless=None):
        self.anylist_properties = {'name': 'meetme',
                                   'urloptions': (1, 5, True)}
        AnyList.__init__(self, newurls)
        InviteConfroom.register_callback(self.invite)

    def update(self):
        ret = AnyList.update(self)
        self.reverse_index = {}
        for idx, ag in self.keeplist.iteritems():
            if ag['confno'] not in self.reverse_index:
                self.reverse_index[ag['confno']] = idx
            else:
                logger.warning('2 meetme have the same room number')
        return ret

    def update_computed_fields(self, newlist):
        for item in newlist.itervalues():
            item['pin_needed'] = 'pin' in item and len(item['pin']) > 0

    def idbyroomnumber(self, roomnumber):
        idx = self.reverse_index.get(roomnumber)
        if idx in self.keeplist:
            return idx

    def invite(self, invite_confroom_command):
        ami = self._ctiserver.myami[self._ipbxid].amicl
        params = [('Channel', 'SIP/eh51sh'),
                  ('Exten', '800'),
                  ('Context', 'default'),
                  ('Priority', '1'),
                  ('CallerID', 'Meetme')]

        if ami.sendcommand('originate', params):
            message = {'class': 'invite_confroom',
                       'message': 'Command sent succesfully'}
            if invite_confroom_command._commandid:
                message['replyid'] = invite_confroom_command._commandid
            return {'message': message}
        else:
            message = {'class': 'invite_confroom',
                       'message': 'AMI sendcommand failed'}
            if invite_confroom_command._commandid:
                message['replyid'] = invite_confroom_command._commandid
            return {'warning': message}

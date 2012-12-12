# -*- coding: utf-8 -*-

# XiVO CTI Server
#
# Copyright (C) 2007-2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Alternatively, XiVO CTI Server is available under other licenses directly
# contracted with Avencall. See the LICENSE file at top of the souce tree
# or delivered in the installable package in which XiVO CTI Server is
# distributed for more details.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from mock import Mock
from xivo_cti.services.agent_availability_notifier import AgentAvailabilityNotifier
from xivo_cti.services.agent_status import AgentStatus
from xivo_cti.cti.cti_message_formatter import CTIMessageFormatter
from xivo_cti.ctiserver import CTIServer
from xivo_cti.dao.innerdata_dao import InnerdataDAO


class TestAgentAvailabilityNotifier(unittest.TestCase):

    def test_notify(self):
        agent_id = 42
        mock_cti_message_formatter = Mock(CTIMessageFormatter)
        mock_innerdata_dao = Mock(InnerdataDAO)
        mock_cti_server = Mock(CTIServer)
        agent_availability_notifier = AgentAvailabilityNotifier(mock_innerdata_dao,
                                                                mock_cti_server,
                                                                mock_cti_message_formatter)
        new_agent_status = {'availability': AgentStatus.logged_out,
                            'availability_since': 123456789}
        mock_innerdata_dao.agent_status.return_value = new_agent_status
        cti_message = {'class': 'getlist',
                       'listname': 'agents',
                       'function': 'updatestatus',
                       'tipbxid': 'xivo',
                       'tid': agent_id,
                       'status': new_agent_status}
        mock_cti_message_formatter.update_agent_status.return_value = cti_message

        agent_availability_notifier.notify(agent_id)

        mock_cti_message_formatter.update_agent_status.assert_called_once_with(agent_id,
                                                                               new_agent_status)
        mock_cti_server.send_cti_event.assert_called_once_with(cti_message)

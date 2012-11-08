# -*- coding: utf-8 -*-

# Copyright (C) 2007-2012  Avencall

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


class AgentDAO(object):
    def __init__(self, innerdata, queue_member_dao):
        self.innerdata = innerdata
        self.queue_member_dao = queue_member_dao

    def get_id_from_number(self, agent_number):
        agent_list = self.innerdata.xod_config['agents'].keeplist
        for (agent_id, agent) in agent_list.iteritems():
            if agent['number'] == agent_number:
                return int(agent_id)

    def get_interface_from_id(self, agent_id):
        agent_list = self.innerdata.xod_config['agents'].keeplist
        agent_number = agent_list[str(agent_id)]['number']
        return 'Agent/%s' % agent_number

    def is_completely_paused(self, agent_id):
        agent_interface = self.get_interface_from_id(agent_id)

        agent_membership_count = self.queue_member_dao.get_queue_count_for_agent(agent_interface)
        if agent_membership_count == 0:
            return False

        paused_count = self.queue_member_dao.get_paused_count_for_agent(agent_interface)
        return paused_count == agent_membership_count

# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>


class CTIMessageFormatter(object):

    @staticmethod
    def add_queue_members(queue_member_ids):
        return {
            'class': 'getlist',
            'listname': 'queuemembers',
            'function': 'addconfig',
            'tipbxid': 'xivo',
            'list': list(queue_member_ids),
        }

    @staticmethod
    def dial_success(exten):
        return {
            'class': 'dial_success',
            'exten': exten,
        }

    @staticmethod
    def delete_queue_members(queue_member_ids):
        return {
            'class': 'getlist',
            'listname': 'queuemembers',
            'function': 'delconfig',
            'tipbxid': 'xivo',
            'list': list(queue_member_ids),
        }

    @staticmethod
    def update_agent_status(agent_id, agent_status):
        return {'class': 'getlist',
                'listname': 'agents',
                'function': 'updatestatus',
                'tipbxid': 'xivo',
                'tid': agent_id,
                'status': agent_status}

    @staticmethod
    def update_queue_member_config(queue_member):
        return {
            'class': 'getlist',
            'listname': 'queuemembers',
            'function': 'updateconfig',
            'tipbxid': 'xivo',
            'tid': queue_member.id,
            'config': queue_member.to_cti_config(),
        }

    @staticmethod
    def ipbxcommand_error(msg):
        return {
            'class': 'ipbxcommand',
            'error_string': msg,
        }

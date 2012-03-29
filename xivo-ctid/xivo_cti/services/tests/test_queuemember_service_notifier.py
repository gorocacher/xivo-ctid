#!/usr/bin/python
# vim: set fileencoding=utf-8 :

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

import unittest
import Queue
from mock import Mock, call, ANY
from xivo_cti.services.queuemember_service_notifier import QueueMemberServiceNotifier
from xivo_cti.tools.delta_computer import DictDelta

class TestQueueMemberServiceNotifier(unittest.TestCase):

    def setUp(self):
        self.ipbx_id = 'xivo_test'
        self.notifier = QueueMemberServiceNotifier()
        self.notifier.ipbx_id = self.ipbx_id
        self.notifier.innerdata_dao = Mock()
        self.notifier.events_cti = Queue.Queue()


    def test_queuemember_config_updated_add(self):
        input_delta = DictDelta({'key1': 'value1', 'key2': 'value2'}, {}, [])
        expected_cti_event = {'class': 'getlist',
                              'function': 'addconfig',
                              'listname': 'queuemembers',
                              'list': ['key1', 'key2'],
                              'tipbxid': self.ipbx_id
                              }

        self.notifier.queuemember_config_updated(input_delta)

        innerdata_method_calls = self.notifier.innerdata_dao.method_calls
        cti_event = self.notifier.events_cti.get()
        self.assertEqual(innerdata_method_calls, [call.apply_queuemember_delta(ANY)])
        self.assertEqual(cti_event, expected_cti_event)

    def test_queuemember_config_updated_delete(self):
        input_delta = DictDelta({}, {}, ['key1', 'key2'])
        expected_cti_event = {'class': 'getlist',
                              'function': 'delconfig',
                              'listname': 'queuemembers',
                              'list': ['key1', 'key2'],
                              'tipbxid': self.ipbx_id
                              }

        self.notifier.queuemember_config_updated(input_delta)

        innerdata_method_calls = self.notifier.innerdata_dao.method_calls
        cti_event = self.notifier.events_cti.get()
        self.assertEqual(innerdata_method_calls, [call.apply_queuemember_delta(ANY)])
        self.assertEqual(cti_event, expected_cti_event)

    def test_queuemember_config_updated_change(self):
        input_delta = DictDelta({}, {'key1': 'value1', 'key2': 'value2'}, [])
        expected_cti_event = {'class': 'getlist',
                              'function': 'updateconfig',
                              'listname': 'queuemembers',
                              'config': input_delta.change,
                              'tipbxid': self.ipbx_id
                              }

        self.notifier.queuemember_config_updated(input_delta)

        innerdata_method_calls = self.notifier.innerdata_dao.method_calls
        cti_event = self.notifier.events_cti.get()
        self.assertEqual(innerdata_method_calls, [call.apply_queuemember_delta(ANY)])
        self.assertEqual(cti_event, expected_cti_event)

    def test_queuemember_config_updated_add_and_delete(self):
        input_delta = DictDelta({'key1': 'value1', 'key2': 'value2'}, {}, ['key3'])
        expected_cti_events = [{'class': 'getlist',
                              'function': 'addconfig',
                              'listname': 'queuemembers',
                              'list': ['key1', 'key2'],
                              'tipbxid': self.ipbx_id
                              },
                              {'class': 'getlist',
                              'function': 'delconfig',
                              'listname': 'queuemembers',
                              'list': input_delta.delete,
                              'tipbxid': self.ipbx_id
                              }]

        self.notifier.queuemember_config_updated(input_delta)

        innerdata_method_calls = self.notifier.innerdata_dao.method_calls
        cti_events = []
        while not self.notifier.events_cti.empty():
            cti_events.append(self.notifier.events_cti.get())
        self.assertEqual(innerdata_method_calls, [call.apply_queuemember_delta(ANY)])
        self.assertEqual(cti_events, expected_cti_events)

    def test_queuemember_config_updated_add_and_change(self):
        input_delta = DictDelta({'key1': 'value1', 'key2': 'value2'}, {'key3':'value3', 'key4': 'value4'}, [])
        expected_cti_events = [{'class': 'getlist',
                              'function': 'addconfig',
                              'listname': 'queuemembers',
                              'list': ['key1', 'key2'],
                              'tipbxid': self.ipbx_id
                              },
                              {'class': 'getlist',
                              'function': 'updateconfig',
                              'listname': 'queuemembers',
                              'config': input_delta.change,
                              'tipbxid': self.ipbx_id
                              }]

        self.notifier.queuemember_config_updated(input_delta)

        innerdata_method_calls = self.notifier.innerdata_dao.method_calls
        cti_events = []
        while not self.notifier.events_cti.empty():
            cti_events.append(self.notifier.events_cti.get())
        self.assertEqual(innerdata_method_calls, [call.apply_queuemember_delta(ANY)])
        self.assertEqual(cti_events, expected_cti_events)

    def test_queuemember_config_updated_delete_and_change(self):
        input_delta = DictDelta({}, {'key1': 'value1', 'key2': 'value2'}, ['key3', 'key4'])
        expected_cti_events = [{'class': 'getlist',
                              'function': 'updateconfig',
                              'listname': 'queuemembers',
                              'config': input_delta.change,
                              'tipbxid': self.ipbx_id
                              },
                              {'class': 'getlist',
                              'function': 'delconfig',
                              'listname': 'queuemembers',
                              'list': input_delta.delete,
                              'tipbxid': self.ipbx_id
                              }]

        self.notifier.queuemember_config_updated(input_delta)

        innerdata_method_calls = self.notifier.innerdata_dao.method_calls
        cti_events = []
        while not self.notifier.events_cti.empty():
            cti_events.append(self.notifier.events_cti.get())
        self.assertEqual(innerdata_method_calls, [call.apply_queuemember_delta(ANY)])
        self.assertEqual(cti_events, expected_cti_events)

    def test_queuemember_config_updated_add_change_and_delete(self):
        input_delta = DictDelta({'key1': 'value1'}, {'key2':'value2'}, ['key3'])
        expected_cti_events = [{'class': 'getlist',
                              'function': 'addconfig',
                              'listname': 'queuemembers',
                              'list': ['key1'],
                              'tipbxid': self.ipbx_id
                              },
                              {'class': 'getlist',
                              'function': 'updateconfig',
                              'listname': 'queuemembers',
                              'config': input_delta.change,
                              'tipbxid': self.ipbx_id
                              },
                              {'class': 'getlist',
                              'function': 'delconfig',
                              'listname': 'queuemembers',
                              'list': input_delta.delete,
                              'tipbxid': self.ipbx_id
                              },]

        self.notifier.queuemember_config_updated(input_delta)

        innerdata_method_calls = self.notifier.innerdata_dao.method_calls
        cti_events = []
        while not self.notifier.events_cti.empty():
            cti_events.append(self.notifier.events_cti.get())
        self.assertEqual(innerdata_method_calls, [call.apply_queuemember_delta(ANY)])
        self.assertEqual(cti_events, expected_cti_events)

    def test_request_queuemembers_to_ami_empty(self):
        queuemembers_list = []
        self.notifier.interface_ami = Mock()
        expected_ami_method_calls = []

        self.notifier.request_queuemembers_to_ami(queuemembers_list)

        ami_method_calls = self.notifier.interface_ami.method_calls
        self.assertEqual(ami_method_calls, expected_ami_method_calls)

    def test_request_queuemembers_to_ami_full(self):
        queuemembers_list = [('agent1', 'queue1'), ('agent2', 'queue2')]
        params1 = {'mode': 'request_queuemember',
                   'amicommand': 'sendcommand',
                   'amiargs': ('queuestatus', [('Member', 'agent1'),
                                               ('Queue', 'queue1')])}
        params2 = {'mode': 'request_queuemember',
                   'amicommand': 'sendcommand',
                   'amiargs': ('queuestatus', [('Member', 'agent2'),
                                               ('Queue', 'queue2')])}
        self.notifier.interface_ami = Mock()
        expected_ami_method_calls = [call.execute_and_track(ANY, params1),
                                     call.execute_and_track(ANY, params2)]

        self.notifier.request_queuemembers_to_ami(queuemembers_list)

        ami_method_calls = self.notifier.interface_ami.method_calls
        self.assertEqual(ami_method_calls, expected_ami_method_calls)

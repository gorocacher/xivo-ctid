# -*- coding: utf-8 -*-

# Copyright (C) 2007-2013 Avencall
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

import unittest

from mock import Mock, call, sentinel
from hamcrest import *

from xivo_cti import innerdata
from xivo_cti import channel_updater
from xivo_cti.channel import Channel
from xivo_cti.channel_updater import assert_has_channel


class TestAssertHasChannelDecorator(unittest.TestCase):

    def setUp(self):
        self.original = Mock()
        self.decorated = assert_has_channel(self.original)
        self.channel_name = 'SIP/abc-123'
        self.updater = Mock()

    def test_assert_has_channel(self):
        self.updater.innerdata.channels = {self.channel_name: 1}

        self.decorated(self.updater, self.channel_name, sentinel.arg)

        self.original.assert_called_once_with(self.updater, self.channel_name, sentinel.arg)

    def test_assert_has_channel_not_found(self):
        self.updater.innerdata.channels = {}

        self.decorated(self.updater, self.channel_name, sentinel.arg)

        self.assertFalse(self.original.called)


class TestChannelUpdater(unittest.TestCase):

    def setUp(self):
        self.innerdata = Mock(innerdata.Safe)
        self.innerdata.channels = {}
        self.updater = channel_updater.ChannelUpdater(self.innerdata)

    def test_new_caller_id(self):
        channel_1 = {
            'name': 'SIP/abc-124',
            'context': 'test',
            'unique_id': 12798734.33
        }
        self.innerdata.channels = {
            channel_1['name']: Channel(channel_1['name'],
                                       channel_1['context'],
                                       channel_1['unique_id'])
        }

        self.updater.new_caller_id(channel_1['name'],
                                   'Alice',
                                   '1234')

        channel = self.innerdata.channels[channel_1['name']]
        self.assertEqual(channel.extra_data['xivo']['calleridname'], 'Alice')
        self.assertEqual(channel.extra_data['xivo']['calleridnum'], '1234')

    def test_new_caller_id_unknown_channel(self):
        self.updater.new_caller_id('SIP/1234', 'Alice', '1234')

    def test_hold_channel(self):
        name, status = 'SIP/1234', True
        channel = Channel(name, 'default', '123456.66')
        self.innerdata.channels[name] = channel

        self.updater.set_hold(name, status)

        channel = self.innerdata.channels[name]
        assert_that(channel.properties['holded'], equal_to(status), 'holded status')
        self._assert_channel_updated(name)

    def _assert_channel_updated(self, channel):
        calls = list(self.innerdata.handle_cti_stack.call_args_list)
        expected = [call('setforce', ('channels', 'updatestatus', channel)),
                    call('empty_stack')]

        assert_that(calls, equal_to(expected), 'handle_cti_stack calls')

    def test_inherit_channels(self):
        parent_name = 'SIP/parent_channel-0'
        parent = Mock(Channel)
        self.innerdata.channels[parent_name] = parent
        child_name = 'SIP/child_channel-0'
        child = Mock(Channel)
        self.innerdata.channels[child_name] = child

        self.updater.inherit_channels(parent_name, child_name)

        new_child = self.innerdata.channels[child_name]
        new_child.inherit.assert_called_once_with(parent)

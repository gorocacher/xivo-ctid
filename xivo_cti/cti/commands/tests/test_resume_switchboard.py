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

import unittest

from xivo_cti.cti.commands.resume_switchboard import ResumeSwitchboard


class TestResumeSwitchboard(unittest.TestCase):

    def setUp(self):
        self.commandid = 125731893
        self.resume_switchboard_message = {
            'class': 'resume_switchboard',
            'unique_id': '123456.66',
            'commandid': self.commandid,
        }

    def test_from_dict(self):
        resume_switchboard = ResumeSwitchboard.from_dict(self.resume_switchboard_message)

        self.assertEqual(resume_switchboard.commandid, self.commandid)
        self.assertEqual(resume_switchboard.unique_id, self.resume_switchboard_message['unique_id'])

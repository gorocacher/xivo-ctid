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

from xivo_cti.cti.commands.directory import Directory


class TestDirectory(unittest.TestCase):

    _command_id = 1171069123
    _pattern = 'Test'
    _msg_dict = {'class': Directory.class_name, 'pattern': _pattern}

    def test_from_dict(self):
        directory = Directory.from_dict(self._msg_dict)

        self.assertEqual(directory.pattern, self._pattern)

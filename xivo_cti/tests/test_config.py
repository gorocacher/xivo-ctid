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

from xivo_cti.cti_config import _DbConfig as Config
from mock import patch


class TestConfig(unittest.TestCase):

    @patch('xivo_dao.cti_service_dao.get_services')
    def test_get_services(self, mock_get_services_dao):
        expected_result = {
            "itm_services_agent": [""],
            "itm_services_client": ["enablednd",
                                    "fwdunc",
                                    "fwdbusy",
                                    "fwdrna"]
        }

        mock_get_services_dao.return_value = {
            "agent": [],
            "client": ["enablednd",
                       "fwdunc",
                       "fwdbusy",
                       "fwdrna"]
        }

        config = Config()

        result = config._get_services()

        mock_get_services_dao.assert_called_once_with()

        self.assertEquals(result, expected_result)

    @patch('xivo_dao.cti_preference_dao.get_preferences')
    def test_get_preferences(self, mock_get_preferences_dao):
        expected_result = {
            "itm_preferences_agent": False,
            "itm_preferences_client": {
                "xlet.identity.logagent": "1",
                "xlet.identity.pauseagent": "1"
            }
        }

        mock_get_preferences_dao.return_value = {
            "agent": {},
            "client": {
                "xlet.identity.logagent": "1",
                "xlet.identity.pauseagent": "1"
            }
        }

        config = Config()

        result = config._get_preferences()

        mock_get_preferences_dao.assert_called_once_with()

        self.assertEquals(result, expected_result)

    @patch('xivo_dao.cti_profile_dao.get_profiles')
    def test_get_profiles(self, mock_get_profiles_dao):
        expected_result = {
            "client": {
                "name": "Client",
                "phonestatus": "xivo",
                "userstatus": "xivo",
                "preferences": "itm_preferences_client",
                "services": "itm_services_client",
                "xlets": [
                    [
                        "tabber",
                        "grid",
                        "1"
                    ],
                    [
                        "agentdetails",
                        "dock",
                        "cms"
                    ]
                ]
            }
        }

        mock_get_profiles_dao.return_value = {
            "client": {
                "name": "Client",
                "phonestatus": "xivo",
                "userstatus": "xivo",
                "preferences": "itm_preferences_client",
                "services": "itm_services_client",
                "xlets": [
                    {'name': 'tabber',
                     'layout': 'grid',
                     'floating': True,
                     'closable': True,
                     'movable': True,
                     'scrollable': True,
                     'order': 1},
                    {'name': 'agentdetails',
                     'layout': 'dock',
                     'floating': False,
                     'closable': True,
                     'movable': True,
                     'scrollable': True,
                     'order': 0}
                ]
            }
        }

        config = Config()

        result = config._get_profiles()

        mock_get_profiles_dao.assert_called_once_with()

        self.assertEquals(result, expected_result)

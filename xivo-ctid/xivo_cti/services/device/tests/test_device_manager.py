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
import mock

from mock import patch
from mock import Mock

from xivo_cti.services.device.manager import DeviceManager
from xivo_cti.services.device.controller.aastra import AastraController
from xivo_dao.data_handler.device.model import Device
from xivo_dao.data_handler.exception import ElementNotExistsError
from xivo_cti.xivo_ami import AMIClass


class TestDeviceManager(unittest.TestCase):

    def setUp(self):
        self.aastra_controller = mock.Mock(AastraController)
        self.ami_class = Mock(AMIClass)
        self.manager = DeviceManager(self.ami_class)
        self.manager.aastra_controller = self.aastra_controller

    @patch('xivo_dao.data_handler.device.services.get')
    def test_answer(self, mock_device_service_get):
        device_id = 13
        mock_device_service_get.return_value = device = Device(id=device_id)
        self.manager.is_supported_device = mock.Mock(return_value=True)

        self.manager.answer(device_id)

        self.aastra_controller.answer.assert_called_once_with(device)

    @patch('xivo_dao.data_handler.device.services.get')
    def test_answer_with_unsupported_device(self, mock_device_service_get):
        device_id = 13
        mock_device_service_get.return_value = Device(id=device_id)
        self.manager.is_supported_device = Mock(return_value=False)

        self.manager.answer(device_id)

        self.manager.is_supported_device.assert_called_once_with(device_id)

        self.assertEquals(self.aastra_controller.answer.call_count, 0)

    @patch('xivo_dao.data_handler.device.services.get',
           Mock(side_effect=ElementNotExistsError('Not found')))
    def test_answer_no_configured_device(self):

        self.manager.answer(5)

        self.assertEquals(self.aastra_controller.answer.call_count, 0)

    @patch('xivo_dao.data_handler.device.services.get')
    def test_is_supported_device_6731i(self, device_services_get):
        device = Device(id=13,
                        vendor='Aastra',
                        model='6731i')

        device_services_get.return_value = device

        result = self.manager.is_supported_device(device.id)

        self.assertEqual(result, True)

    @patch('xivo_dao.data_handler.device.services.get')
    def test_is_supported_device_6757i(self, device_services_get):
        device = Device(id=13,
                        vendor='Aastra',
                        model='6757i')

        device_services_get.return_value = device

        result = self.manager.is_supported_device(device.id)

        self.assertEqual(result, True)

    @patch('xivo_dao.data_handler.device.services.get')
    def test_is_supported_device_6755i(self, device_services_get):
        device = Device(id=13,
                        vendor='Aastra',
                        model='6755i')

        device_services_get.return_value = device

        result = self.manager.is_supported_device(device.id)

        self.assertEqual(result, True)

    @patch('xivo_dao.data_handler.device.services.get')
    def test_is_supported_device_snom_720(self, device_services_get):
        device = Device(id=13,
                        vendor='Snom',
                        model='720')

        device_services_get.return_value = device

        result = self.manager.is_supported_device(device.id)

        self.assertEqual(result, True)

    @patch('xivo_dao.data_handler.device.services.get')
    def test_is_not_supported_device(self, device_services_get):
        device = Device(id=13,
                        vendor='Cisco',
                        model='1234')

        device_services_get.return_value = device

        result = self.manager.is_supported_device(device.id)

        self.assertEqual(result, False)

    @patch('xivo_dao.data_handler.device.services.get')
    def test_is_supported_device_does_not_exists(self, mock_get):
        def aux(_):
            raise ElementNotExistsError('not found')

        mock_get.side_effect = aux

        result = self.manager.is_supported_device('000deadbeef000')

        self.assertEqual(result, False)

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

import logging
from xivo_cti.client_connection import ClientConnection

logger = logging.getLogger("StatisticsNotifier")


class StatisticsNotifier(object):

    COMMAND_CLASS = 'getqueuesstats'
    CONTENT = 'stats'

    def __init__(self):
        self.cti_connections = set()
        self.closed_cti_connections = set()

    def on_stat_changed(self, statistic):
        for cti_connection in self.cti_connections:
            self.send_statistic(statistic, cti_connection)
        self._remove_closed_connections()

    def subscribe(self, cti_connection):
        logger.info('xivo client subscribing ')
        self.cti_connections.add(cti_connection)

    def send_statistic(self, statistic, cti_connection):
        try:
            cti_connection.send_message({'class': self.COMMAND_CLASS,
                                          self.CONTENT: statistic})
        except ClientConnection.CloseException:
            self.closed_cti_connections.add(cti_connection)

    def _remove_closed_connections(self):
        for closed_connection in self.closed_cti_connections:
            self.cti_connections.remove(closed_connection)
        self.closed_cti_connections.clear()

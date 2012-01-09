# vim: set fileencoding=utf-8 :
# XiVO CTI Server

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

from xivo_cti.cti.missing_field_exception import MissingFieldException


class AMIAction(object):

    _required_fields = []  # Required fields to send this action
    _optionnal_dependencies = []  # List of tupple of mutualy exclusive dependencies see originate

    def __init__(self):
        self.action = None
        self.actionid = None

    def _fields_missing(self):
        for field in self.__class__._required_fields:
            if not hasattr(self, field) or not getattr(self, field):
                return True
        return self._optionnal_dependency_missing()

    def _optionnal_dependency_missing(self):
        for dependency_list in self.__class__._optionnal_dependencies:
            missed_field = False
            for field in dependency_list:
                if not hasattr(self, field) or not getattr(self, field):
                    missed_field = True
            if not missed_field:
                return False
        return True

    def _get_args(self):
        if self._fields_missing():
            raise MissingFieldException('Cannot send AMI action %s' % self.action)
        return []

    def send(self, ami):
        return ami.sendcommand(self.action, self._get_args())

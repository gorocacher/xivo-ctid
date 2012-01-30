# -*- coding: UTF-8 -*-

# XiVO CTI Server
# Copyright (C) 2009-2011  Avencall
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

from xivo_cti.dao.alchemy import dbconnection
from xivo_cti.dao.alchemy.base import Base
from xivo_cti.dao.alchemy.userfeatures import UserFeatures
from xivo_cti.dao.userfeaturesdao import UserFeaturesDAO
from tests.mock import Mock
from xivo_cti.innerdata import Safe
from xivo_cti.lists.cti_userlist import UserList


class Test(unittest.TestCase):

    def setUp(self):
        db_connection_pool = dbconnection.DBConnectionPool(dbconnection.DBConnection)
        dbconnection.register_db_connection_pool(db_connection_pool)

        uri = 'postgresql://asterisk:asterisk@localhost/asterisktest'
        dbconnection.add_connection_as(uri, 'asterisk')
        connection = dbconnection.get_connection('asterisk')

        Base.metadata.drop_all(connection.get_engine(), [UserFeatures().__table__])
        Base.metadata.create_all(connection.get_engine(), [UserFeatures().__table__])

        self.session = connection.get_session()

        self.session.commit()

        self._innerdata = Mock(Safe)
        self._userlist = Mock(UserList)
        self._userlist.keeplist = {}
        self._innerdata.xod_config = {'users': self._userlist}

    def tearDown(self):
        dbconnection.unregister_db_connection_pool()

    def test_set_dnd(self):
        user_id = self._insert_user_dnd_not_set()
        dao = UserFeaturesDAO(self.session)
        dao._innerdata = self._innerdata

        dao.enable_dnd(user_id)

        dbconnection.unregister_db_connection_pool()
        self._check_dnd_is_set(user_id)

    def _insert_user_dnd_not_set(self):
        user_features = UserFeatures()
        user_features.enablednd = 0
        user_features.firstname = 'firstname_test'
        self.session.add(user_features)
        self.session.commit()
        user_id = user_features.id
        self._userlist.keeplist[user_id] = {'enablednd': False}
        return user_id

    def _check_dnd_is_set(self, user_id):
        user_features = (self.session.query(UserFeatures)
                         .filter(UserFeatures.id == user_id))[0]
        self.assertTrue(self._userlist.keeplist[user_id]['enablednd'])
        self.assertTrue(user_features.enablednd)

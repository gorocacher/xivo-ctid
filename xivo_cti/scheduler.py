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

import threading
import os


class Scheduler(object):

    def setup(self, pipe_thread):
        self._pipe_thread = pipe_thread

    def schedule(self, timeout, callback_function, *callback_args):
        callback_args_extended = [callback_function]
        callback_args_extended.extend(callback_args)
        timer = threading.Timer(timeout, self.execute_callback, callback_args_extended)
        timer.start()

    def execute_callback(self, callback_function, *callback_args):
        callback_function(*callback_args)
        self._unlock_select_loop()

    def _unlock_select_loop(self):
        os.write(self._pipe_thread, 'scheduler:callback\n')
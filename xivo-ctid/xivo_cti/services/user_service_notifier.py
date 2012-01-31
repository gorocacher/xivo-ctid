import logging

logger = logging.getLogger('user_service_notifier')


class UserServiceNotifier(object):

    STATUS_MESSAGE = {"class": "getlist",
                   "function": "updateconfig",
                   "listname": "users",
                   "tid": '',
                   "tipbxid": ''}

    def _prepare_dnd_message(self, dnd_status, user_id):
        dnd_enabled_msg = self.STATUS_MESSAGE
        dnd_enabled_msg['config'] = {'enablednd': dnd_status}
        dnd_enabled_msg['tid'] = user_id
        dnd_enabled_msg['tipbxid'] = self.ipbx_id
        return dnd_enabled_msg

    def _prepare_filter_message(self, filter_status, user_id):
        filter_status_msg = self.STATUS_MESSAGE
        filter_status_msg['config'] = {'incallfilter': filter_status}
        filter_status_msg['tid'] = user_id
        filter_status_msg['tipbxid'] = self.ipbx_id
        return filter_status_msg

    def _prepare_unconditional_fwd_message(self, status, destination, user_id):
        filter_status_msg = self.STATUS_MESSAGE
        filter_status_msg.update({'config': {'enableunc': status,
                                             'destunc': destination},
                                  'tid': user_id,
                                  'tipbxid': self.ipbx_id})
        return filter_status_msg

    def dnd_enabled(self, user_id):
        self.events_cti.put(self._prepare_dnd_message(True, user_id))

    def dnd_disabled(self, user_id):
        self.events_cti.put(self._prepare_dnd_message(False, user_id))

    def filter_enabled(self, user_id):
        self.events_cti.put(self._prepare_filter_message(True, user_id))

    def filter_disabled(self, user_id):
        self.events_cti.put(self._prepare_filter_message(False, user_id))

    def unconditional_fwd_enabled(self, user_id, destination):
        self.events_cti.put(self._prepare_unconditional_fwd_message(True, destination, user_id))

    def unconditional_fwd_disabled(self, user_id, destination):
        self.events_cti.put(self._prepare_unconditional_fwd_message(False, destination, user_id))

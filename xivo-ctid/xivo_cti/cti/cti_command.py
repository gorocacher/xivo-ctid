from xivo_cti.cti.missing_field_exception import MissingFieldException


class CTICommand(object):

    required_fields = ['class']
    conditions = None

    def __init__(self, msg):
        self._msg = msg
        self._check_required_fields()
        self._commandid = self._msg.get('commandid')
        self._command_class = self._msg['class']

    def _check_required_fields(self):
        for field in self.__class__.required_fields:
            if field not in self._msg:
                raise MissingFieldException(u'Missing %s in CTI command' % field)

    @classmethod
    def match_message(cls, message):
        if not cls.conditions:
            return False
        for (field, value) in cls.conditions:
            try:
                if not message[field] == value:
                    return False
            except KeyError:
                return False
        return True
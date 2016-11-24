"""PytSite HTTP Session.
"""
from copy import deepcopy as _deepcopy
from werkzeug.contrib.sessions import Session as _BaseSession

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Session(_BaseSession):
    """PytSite HTTP Session.
    """

    def __init__(self, data, sid, new=False):
        """Init.
        """
        self['__flash'] = {}

        super().__init__(data, sid, new)

    def flash_set(self, key: str, value):
        """Set flash value.
        """
        self['__flash'][key] = value
        self.modified = True

        return self

    def flash_get(self, key: str, default=None):
        """Pop flash value.
        """
        r = default

        if key in self['__flash']:
            r = _deepcopy(self['__flash'][key])
            del self['__flash'][key]

        return r

    def flash_clear(self):
        """Clear flash data.
        """
        if '__flash' not in self or self['__flash'] != {}:
            self['__flash'] = {}
            self.modified = True

        return self

    def add_message(self, msg: str, section: str, unique: bool = True):
        """Add a flash message.
        """
        if unique and self.has_message(msg, section):
            return self

        if '__messages' not in self['__flash']:
            self['__flash']['__messages'] = {}

        if section not in self['__flash']['__messages']:
            self['__flash']['__messages'][section] = []

        self['__flash']['__messages'][section].append(msg)
        self.modified = True

        return self

    def add_success_message(self, msg: str, unique: bool = True):
        """Add a success flash message.
        """
        return self.add_message(msg, 'success', unique)

    def add_info_message(self, msg: str, unique: bool = True):
        """Add an info flash message.
        """
        return self.add_message(msg, 'info', unique)

    def add_warning_message(self, msg: str, unique: bool = True):
        """Add a warning flash message.
        """
        return self.add_message(msg, 'warning', unique)

    def add_error_message(self, msg: str, unique: bool = True):
        """Add an error flash message.
        """
        return self.add_message(msg, 'error', unique)

    def has_message(self, msg: str, section: str) -> bool:
        """Check if the session contains a flash message.
        """
        if '__messages' not in self['__flash'] or section not in self['__flash']['__messages']:
            return False

        return msg in self['__flash']['__messages'][section]

    def has_info_message(self, msg: str) -> bool:
        """Check if the session contains an info message.
        """
        return self.has_message(msg, 'info')

    def has_success_message(self, msg: str) -> bool:
        """Check if the session contains a success message.
        """
        return self.has_message(msg, 'success')

    def has_warning_message(self, msg: str) -> bool:
        """Check if teh session contains a warning message.
        """
        return self.has_message(msg, 'warning')

    def has_error_message(self, msg: str) -> bool:
        """Check if the session contains an error message.
        """
        return self.has_message(msg, 'error')

    def get_messages(self, section: str) -> tuple:
        """Pop flash messages.
        """
        r = []

        if '__messages' not in self['__flash']:
            return tuple(r)

        if section in self['__flash']['__messages']:
            r = _deepcopy(self['__flash']['__messages'][section])
            self['__flash']['__messages'][section].clear()
            self.modified = True

        return tuple(r)

    def get_info_messages(self) -> tuple:
        """Pop info messages.
        """
        return self.get_messages('info')

    def get_success_messages(self) -> tuple:
        """Pop success messages.
        """
        return self.get_messages('success')

    def get_warning_messages(self) -> tuple:
        """Pop warning messages.
        """
        return self.get_messages('warning')

    def get_error_messages(self) -> tuple:
        """Pop error messages.
        """
        return self.get_messages('error')

    def get_message(self, msg: str, section: str) -> str:
        """Pop single flash message.
        """
        if not self.has_message(msg, section):
            return

        messages = self['__flash']['__messages'][section]

        return messages.pop(messages.index(msg))

    def get_info_message(self, msg: str) -> str:
        """Pop single info message.
        """
        return self.get_message(msg, 'info')

    def get_success_message(self, msg: str) -> str:
        """Pop single success message.
        """
        return self.get_message(msg, 'success')

    def get_warning_message(self, msg: str) -> str:
        """Pop single warning message.
        """
        return self.get_message(msg, 'warning')

    def get_error_message(self, msg: str) -> str:
        """Pop single error message.
        """
        return self.get_message(msg, 'error')

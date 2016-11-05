from werkzeug.contrib.sessions import Session as _BaseSession

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Session(_BaseSession):
    """HTTP Session.
    """

    def flash_set(self, key: str, value):
        """Set flash value.
        """
        if '__flash' not in self:
            self['__flash'] = {}

        self['__flash'][key] = value
        self.modified = True

        return self

    def flash_get(self, key: str, default = None):
        """Get flash value.
        """
        r = default

        if '__flash' not in self:
            return r

        if key in self['__flash']:
            r = self['__flash'][key]
            del self['__flash'][key]

        return r

    def flash_clear(self):
        """Clear all flash data.
        """
        if '__flash' in self and self['__flash']:
            self['__flash'] = {}
            self.modified = True

        return self

    def add_message(self, msg: str, section: str, unique: bool = True):
        """Add a message to the session store.
        """
        if unique and self.has_message(msg, section):
            return self

        if '__flash' not in self:
            self['__flash'] = {'__messages': {}}

        if '__messages' not in self['__flash']:
            self['__flash']['__messages'] = {}

        if section not in self['__flash']['__messages']:
            self['__flash']['__messages'][section] = []

        self['__flash']['__messages'][section].append(msg)
        self.modified = True

        return self

    def add_success_message(self, msg: str, unique: bool = True):
        """Store a success message.
        """
        return self.add_message(msg, 'success', unique)

    def add_info_message(self, msg: str, unique: bool = True):
        """Store an info message.
        """
        return self.add_message(msg, 'info', unique)

    def add_warning_message(self, msg: str, unique: bool = True):
        """Add a warning message.
        """
        return self.add_message(msg, 'warning', unique)

    def add_error_message(self, msg: str, unique: bool = True):
        """Add an error message.
        """
        return self.add_message(msg, 'error', unique)

    def has_message(self, msg: str, section: str) -> bool:
        """Check if the section contains a message.
        """
        if '__flash' not in self or '__messages' not in self['__flash'] or section not in self['__flash']['__messages']:
            return False

        return msg in self['__flash']['__messages'][section]

    def has_info_message(self, msg: str) -> bool:
        """Check if teh session contains info message.
        """
        return self.has_message(msg, 'info')

    def has_success_message(self, msg: str) -> bool:
        """Check if teh session contains success message.
        """
        return self.has_message(msg, 'success')

    def has_warning_message(self, msg: str) -> bool:
        """Check if teh session contains warning message.
        """
        return self.has_message(msg, 'warning')

    def has_error_message(self, msg: str) -> bool:
        """Check if teh session contains error message.
        """
        return self.has_message(msg, 'error')

    def get_messages(self, section: str) -> tuple:
        """Get session messages.
        """
        r = []

        if '__flash' not in self or '__messages' not in self['__flash']:
            return tuple(r)

        if section in self['__flash']['__messages']:
            r = tuple(self['__flash']['__messages'][section])
            self['__flash']['__messages'][section] = []
            self.modified = True

        return r

    def get_info_messages(self) -> tuple:
        """Get info messages.
        """
        return self.get_messages('info')

    def get_success_messages(self) -> tuple:
        """Get success messages.
        """
        return self.get_messages('success')

    def get_warning_messages(self) -> tuple:
        """Get warning messages.
        """
        return self.get_messages('warning')

    def get_error_messages(self) -> tuple:
        """Get error messages.
        """
        return self.get_messages('error')

"""PytSite HTTP Session
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.contrib.sessions import Session as _BaseSession


class Session(_BaseSession):
    """PytSite HTTP Session.
    """

    def clear_messages(self):
        """Clear flash data
        """
        if '__flash' in self:
            del self['__flash']
            self.modified = True

        return self

    def add_message(self, msg: str, section: str, unique: bool = True):
        """Add a flash message
        """
        if unique and self.has_message(msg, section):
            return self

        if '__flash' not in self:
            self['__flash'] = {}

        if section not in self['__flash']:
            self['__flash'][section] = []

        self['__flash'][section].append(msg)
        self.modified = True

        return self

    def add_success_message(self, msg: str, unique: bool = True):
        """Add a success flash message
        """
        return self.add_message(msg, 'success', unique)

    def add_info_message(self, msg: str, unique: bool = True):
        """Add an info flash message
        """
        return self.add_message(msg, 'info', unique)

    def add_warning_message(self, msg: str, unique: bool = True):
        """Add a warning flash message
        """
        return self.add_message(msg, 'warning', unique)

    def add_error_message(self, msg: str, unique: bool = True):
        """Add an error flash message
        """
        return self.add_message(msg, 'error', unique)

    def has_message(self, msg: str, section: str) -> bool:
        """Check if the session contains a flash message
        """
        if '__flash' not in self or section not in self['__flash']:
            return False

        return msg in self['__flash'][section]

    def get_messages(self, section: str) -> tuple:
        """Pop flash messages
        """
        if '__flash' not in self:
            return ()

        r = ()

        if section in self['__flash']:
            r = tuple(self['__flash'][section])
            del self['__flash'][section]
            if not self['__flash']:
                del self['__flash']
            self.modified = True

        return r

    def get_info_messages(self) -> tuple:
        """Pop info messages
        """
        return self.get_messages('info')

    def get_success_messages(self) -> tuple:
        """Pop success messages
        """
        return self.get_messages('success')

    def get_warning_messages(self) -> tuple:
        """Pop warning messages
        """
        return self.get_messages('warning')

    def get_error_messages(self) -> tuple:
        """Pop error messages
        """
        return self.get_messages('error')

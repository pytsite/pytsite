__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.contrib.sessions import Session as Base


class Session(Base):
    """HTTP Session.
    """

    def __init__(self, data, sid, new: bool=False):
        """Init.
        """

        super().__init__(data, sid, new)
        if '__session' not in self:
            self['__session'] = {'__messages': {
                '__success': [],
                '__info': [],
                '__warning': [],
                '__error': []
            }}

    def flash_set(self, key: str, value):
        """Set flash value.
        """

        self['__session'][key] = value
        self.modified = True

        return self

    def flash_get(self, key: str, default=None):
        """Get flash value.
        """
        r = default
        if key in self['__session']:
            r = self['__session'][key]
            del self['__session'][key]

        return r

    def add_message(self, msg: str, section: str):
        """Add a message to the session store.
        """

        self['__session']['__messages']['__' + section].append(msg)
        self.modified = True
        return self

    def add_success(self, msg: str):
        """Store a success message.
        """

        return self.add_message(msg, 'success')

    def add_info(self, msg: str):
        """Store an info message.
        """

        return self.add_message(msg, 'info')

    def add_warning(self, msg: str):
        """Add a warning message.
        """

        return self.add_message(msg, 'warning')

    def add_error(self, msg: str):
        """Add an error message.
        """

        return self.add_message(msg, 'error')

    def get_messages(self, section: str) -> list:
        """Get session messages.
        """

        r = []
        key = '__' + section
        if key in self['__session']['__messages']:
            r = tuple(self['__session']['__messages'][key])
            self['__session']['__messages'][key] = []
            self.modified = True

        return r

    def get_info(self) -> list:
        """Get info messages.
        """

        return self.get_messages('info')

    def get_success(self) -> list:
        """Get success messages.
        """

        return self.get_messages('success')

    def get_warnings(self) -> list:
        """Get warning messages.
        """

        return self.get_messages('warning')

    def get_errors(self) -> list:
        """Get error messages.
        """

        return self.get_messages('error')

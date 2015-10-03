"""Basic Validation Rules.
"""
import re as _re
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import util as _util
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Base(_ABC):
    """Base Rule.
    """
    def __init__(self, value=None, msg_id: str=None):
        """Init.
        """
        self._value = value
        self._msg_id = msg_id if msg_id else 'pytsite.validation@validation_' + self.__class__.__name__.lower()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Set rule's value.
        """
        self._value = value

    @_abstractmethod
    def validate(self):
        pass


class NonEmpty(Base):
    """Not empty rule.
    """
    def validate(self):
        """Do actual validation of the rule.
        """
        if isinstance(self.value, list):
            self.value = _util.list_cleanup(self.value)
        elif isinstance(self.value, dict):
            self.value = _util.dict_cleanup(self.value)
        elif isinstance(self.value, str):
            self.value = self.value.strip()

        if not self._value:
            raise _error.RuleError(self._msg_id)


class DictPartsNotEmpty(Base):
    """Check if a dict particular key values are not empty.
    """
    def __init__(self, value: None, msg_id: str=None, keys: tuple=()):
        """Init.
        """
        super().__init__(value, msg_id)
        self._keys = keys

    def validate(self):
        """Do actual validation of the rule.
        """
        if not isinstance(self._value, dict):
            raise ValueError('Dict expected.')

        # Nothing to validate
        if not self._keys:
            return

        for k in self._keys:
            if k not in self._value or not self._value[k]:
                raise _error.RuleError(self._msg_id, {'keys': self._keys})


class Integer(Base):
    """Integer Validation Rule.
    """
    def validate(self):
        """Do actual validation of the rule.
        """
        try:
            int(self._value)
        except ValueError:
            raise _error.RuleError(self._msg_id)


class Float(Base):
    """Float Validation Rule.
    """
    def validate(self):
        """Do actual validation of the rule.
        """
        try:
            float(self._value)
        except ValueError:
            raise _error.RuleError(self._msg_id)


class Regex(Base):
    def __init__(self, value: str=None, msg_id: str=None, pattern: str='', ignore_case=False):
        super().__init__(value, msg_id)
        self._pattern = pattern
        self._ignore_case = ignore_case

        if not self._pattern or not isinstance(self._pattern, str):
            raise ValueError('Pattern must be a nonempty string.')

        self._regex = _re.compile(self._pattern, _re.IGNORECASE) if self._ignore_case else _re.compile(self._pattern)

    def validate(self):
        """Do actual validation of the rule.
        """
        if not self.value:
            return

        if isinstance(self.value, list):
            self._msg_id += '_row'
            self.value = _util.list_cleanup(self.value)
            for k, v in enumerate(self.value):
                if not self._regex.match(v):
                    raise _error.RuleError(self._msg_id, {'row': k + 1, 'pattern': self._pattern})
        elif isinstance(self.value, dict):
            self._msg_id += '_row'
            self.value = _util.dict_cleanup(self.value)
            for k, v in self.value.items():
                if not self._regex.match(v):
                    raise _error.RuleError(self._msg_id, {'row': k + 1, 'pattern': self._pattern})
        elif isinstance(self.value, str):
            if not self._regex.match(self.value):
                raise _error.RuleError(self._msg_id, {'pattern': self._pattern})
        else:
            raise ValueError('List, dict or str expected.')


class Url(Regex):
    """URL rule.
    """
    def __init__(self, value: str=None, msg_id: str=None):
        pattern = ('^(?:http|ftp)s?://'  # http:// or https://
                   '(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain
                   'localhost|'  # localhost...
                   '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                   '(?::\d+)?'  # optional port
                   '(?:/?|[/?]\S+)$')

        super().__init__(value, msg_id, pattern, True)


class VideoHostingUrl(Url):
    """Video hosting URL rule.
    """
    def validate(self):
        """Do actual validation of the rule.
        """
        super().validate()

        if isinstance(self.value, list):
            for k, v in enumerate(self.value):
                if not self._validate_str(v):
                    raise _error.RuleError(self._msg_id, {'row': k + 1})
        elif isinstance(self.value, dict):
            for k, v in self.value.items():
                if not self._validate_str(v):
                    raise _error.RuleError(self._msg_id, {'row': k + 1})
        elif isinstance(self.value, str):
            if not self._validate_str(self.value):
                raise _error.RuleError(self._msg_id)
        else:
            raise ValueError('List, dict or str expected.')

    def _validate_str(self, inp: str):
        for re in self._get_re():
            if re.search(inp):
                return True

        return False

    @staticmethod
    def _get_re() -> list:
        patterns = (
            '(youtu\.be|youtube\.com)/(watch\?v=)?.{11}',
            'vimeo.com/\d+',
            'rutube.ru/video/\w{32}'
        )
        r = []
        for p in patterns:
            r.append(_re.compile(p, _re.IGNORECASE))

        return r


class Email(Regex):
    """Email rule.
    """
    def __init__(self, value: str=None, msg_id: str=None):
        super().__init__(value, msg_id, '^[0-9a-zA-Z\-_\.+]+@[0-9a-zA-Z\-]+\.[a-z0-9]+$', True)


class DateTime(Base):
    """Date/time Rule.
    """
    def validate(self):
        """Do actual validation of the rule.
        """
        from datetime import datetime
        if isinstance(self._value, str):
            if not _re.match(r'\d{2}\.\d{2}\.\d{4}\s\d{2}\.\d{2}', self._value):
                raise _error.RuleError(self._msg_id)
        elif not isinstance(self._value, datetime):
            raise _error.RuleError(self._msg_id)


class FloatGreaterThan(Float):
    def __init__(self, value: float=None, msg_id: str=None, than=0.0):
        """Init.
        """
        super().__init__(value, msg_id)
        self._than = than

    def validate(self):
        """Do actual validation of the rule.
        """
        super().validate()
        if self.value <= self._than:
            raise _error.RuleError(self._msg_id, {'than': str(self._than)})


class ListListItemNotEmpty(Base):
    def __init__(self, value: list=None, msg_id: str=None, sub_list_item_index: int=0):
        """Init.
        """
        super().__init__(value, msg_id)
        self._index = sub_list_item_index

    def validate(self):
        """Do actual validation of the rule.
        """
        if not isinstance(self.value, list):
            raise ValueError('List expected.')

        for row, sub_list in enumerate(self.value):
            if not isinstance(sub_list, list):
                raise ValueError('List expected.')

            if self._index + 1 > len(sub_list):
                raise _error.RuleError(self._msg_id, {'row': row + 1, 'col': self._index + 1})

            if not sub_list[self._index]:
                raise _error.RuleError(self._msg_id, {'row': row + 1, 'col': self._index + 1})


class ListListItemUrl(ListListItemNotEmpty):
    def validate(self):
        """Do actual validation of the rule.
        """
        if not isinstance(self.value, list):
            raise ValueError('List expected.')

        for row, sub_list in enumerate(self.value):
            if not isinstance(sub_list, list):
                raise ValueError('List expected.')

            if self._index + 1 > len(sub_list):
                raise _error.RuleError(self._msg_id, {'row': row + 1, 'col': self._index + 1})

            url_rule = Url(self._msg_id, sub_list[self._index])
            if not url_rule.validate():
                raise _error.RuleError(self._msg_id, {'row': row + 1, 'col': self._index + 1})

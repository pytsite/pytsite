"""Basic Validation Rules.
"""
import re as _re
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from decimal import Decimal as _Decimal
from pytsite import util as _util, lang as _lang
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_re_num = _re.compile('^\-?\d+(\.\d+)?$')
_re_int_num = _re.compile('^\-?\d+$')
_re_decimal_num = _re.compile('^\-?\d+\.\d+$')


class Base(_ABC):
    """Base Rule.
    """

    def __init__(self, value=None, msg_id: str = None, msg_args: dict = None):
        """Init.
        """
        self._value = value
        self._msg_id = msg_id if msg_id else 'pytsite.validation@validation_' + self.__class__.__name__.lower()
        self._msg_args = msg_args if msg_args is not None else {}

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        """Set rule's value.
        """
        self._value = value

    def validate(self, value=None):
        if value is not None:
            self._value = value

        self._do_validate()

        return self._value

    @_abstractmethod
    def _do_validate(self):
        pass


class Pass(Base):
    """Rule which always passes.
    """

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        pass


class NonEmpty(Base):
    """Not empty rule.
    """

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if type(self._value) in (int, float):
            return self._value

        if isinstance(self._value, list):
            self._value = _util.cleanup_list(self._value)
        elif isinstance(self._value, dict):
            self._value = _util.cleanup_dict(self._value)
        elif isinstance(self._value, str):
            self._value = self._value.strip()

        if not self._value:
            raise _error.RuleError(self._msg_id, self._msg_args)


class Length(Base):
    def __init__(self, value=None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args)

        self._min_length = kwargs.get('min_length')
        self._max_length = kwargs.get('max_length')
        self._msg_args.update({
            'min_length': self._min_length,
            'max_length': self._max_length,
        })

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        try:
            value_len = len(self._value)
        except TypeError:
            raise TypeError("This rule doesn't support values of type '{}'".format(type(self._value).__name__))

        if self._min_length is not None and value_len < self._min_length:
            raise _error.RuleError(self._msg_id, self._msg_args)

        if self._max_length is not None and value_len > self._max_length:
            raise _error.RuleError(self._msg_id, self._msg_args)


class MinLength(Length):
    def __init__(self, value=None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args, min_length=kwargs.get('min_length'))


class MaxLength(Length):
    def __init__(self, value=None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args, max_length=kwargs.get('max_length'))


class DictPartsNonEmpty(Base):
    """Check if a dict particular keys' values are not empty.
    """

    def __init__(self, value=None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args)
        self._keys = kwargs.get('keys', ())
        self._msg_args.update({'keys': self._keys})

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None or not self._keys:
            return

        if not isinstance(self._value, dict):
            raise TypeError(_lang.t('pytsite.validation@dict_expected', {'got': self.value.__class__.__name__}))

        for k in self._keys:
            if k not in self._value or not self._value[k]:
                raise _error.RuleError(self._msg_id, self._msg_args)


class Number(Base):
    """Number validation rule.
    """

    def _do_validate(self):
        if self._value is None:
            return

        if isinstance(self._value, str):
            if not _re_num.match(self._value):
                raise _error.RuleError(self._msg_id)
        elif type(self._value) not in (float, int, _Decimal):
            raise _error.RuleError(self._msg_id, self._msg_args)


class Integer(Base):
    """Integer Validation Rule.
    """

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if isinstance(self._value, str):
            if not _re_int_num.match(self._value):
                raise _error.RuleError(self._msg_id, self._msg_args)
        elif type(self._value) not in (int,):
            raise _error.RuleError(self._msg_id, self._msg_args)


class Decimal(Base):
    """Float Validation Rule.
    """

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if isinstance(self._value, str):
            if not _re_decimal_num.match(self._value):
                raise _error.RuleError(self._msg_id, self._msg_args)
        elif type(self._value) not in (float, _Decimal):
            raise _error.RuleError(self._msg_id, self._msg_args)


class Less(Base):
    def __init__(self, value: float = None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args)
        self._than = kwargs.get('than', 0.0)
        self._msg_args.update({'than': str(self._than)})

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        Number().validate(self._value)
        if float(self._value) >= float(self._than):
            raise _error.RuleError(self._msg_id, self._msg_args)


class LessOrEqual(Less):
    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        Number().validate(self._value)
        if float(self.value) > float(self._than):
            raise _error.RuleError(self._msg_id, self._msg_args)


class Greater(Base):
    def __init__(self, value: float = None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args)
        self._than = kwargs.get('than', 0.0)
        self._msg_args.update({'than': str(self._than)})

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        Number().validate(self._value)
        if float(self.value) <= float(self._than):
            raise _error.RuleError(self._msg_id, self._msg_args)


class GreaterOrEqual(Greater):
    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        Number().validate(self._value)
        if float(self.value) < float(self._than):
            raise _error.RuleError(self._msg_id, self._msg_args)


class Regex(Base):
    def __init__(self, value: str = None, msg_id: str = None, msg_args: dict = None, **kwargs):
        super().__init__(value, msg_id, msg_args)
        self._pattern = kwargs.get('pattern')
        self._ignore_case = kwargs.get('ignore_case', False)
        self._msg_args.update({'pattern': self._pattern})

        if not self._pattern or not isinstance(self._pattern, str):
            raise _error.RuleError('Pattern must be a nonempty string.')

        self._regex = _re.compile(self._pattern, _re.IGNORECASE) if self._ignore_case else _re.compile(self._pattern)

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if isinstance(self.value, (list, tuple)):
            self._msg_id += '_row'
            self.value = _util.cleanup_list(self.value)
            for k, v in enumerate(self.value):
                if not self._regex.match(v):
                    raise _error.RuleError(self._msg_id, dict(self._msg_args, row=k + 1))

        elif isinstance(self.value, dict):
            self._msg_id += '_row'
            self.value = _util.cleanup_dict(self.value)
            for k, v in self.value.items():
                if not self._regex.match(v):
                    raise _error.RuleError(self._msg_id, dict(self._msg_args, row=k + 1))

        elif isinstance(self.value, str):
            value = self.value.strip()
            if value and not self._regex.match(value):
                raise _error.RuleError(self._msg_id, self._msg_args)

        else:
            msg = _lang.t('pytsite.validation@list_dict_str_expected', {'got': self.value.__class__.__name__})
            raise TypeError(msg)


class Url(Regex):
    """URL rule.
    """

    def __init__(self, value: str = None, msg_id: str = None, msg_args: dict = None):
        pattern = ('^(?:http|ftp)s?://'  # http:// or https://
                   '(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
                   'localhost|'  # localhost...
                   '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                   '(?::\d+)?'  # optional port
                   '(?:/?|[/?]\S+)$')

        super().__init__(value, msg_id, msg_args, pattern=pattern, ignore_case=True)


class VideoHostingUrl(Url):
    """Video hosting URL rule.
    """

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self.value is None:
            return

        super()._do_validate()

        if isinstance(self.value, list):
            for k, v in enumerate(self.value):
                if not self._validate_str(v):
                    raise _error.RuleError(self._msg_id, dict(self._msg_args, row=k + 1))
        elif isinstance(self.value, dict):
            for k, v in self.value.items():
                if not self._validate_str(v):
                    raise _error.RuleError(self._msg_id, dict(self._msg_args, row=k + 1))
        elif isinstance(self.value, str):
            if not self._validate_str(self.value):
                raise _error.RuleError(self._msg_id, self._msg_args)
        else:
            msg = _lang.t('pytsite.validation@list_dict_str_expected', {'got': self.value.__class__.__name__})
            raise TypeError(msg)

    def _validate_str(self, inp: str):
        for re in self._get_re():
            if re.search(inp):
                return True

        return False

    @staticmethod
    def _get_re() -> list:
        patterns = (
            '(youtu\.be|youtube\.com)/(watch\?v=)?[0-9a-z-A-Z_-]{11}',
            'facebook\.com/[^/]+/videos/(\d+)',
            'vimeo\.com/\d+',
            'rutube\.ru/video/\w{32}'
        )
        r = []
        for p in patterns:
            r.append(_re.compile(p, _re.IGNORECASE))

        return r


class Email(Regex):
    """Email rule.
    """

    def __init__(self, value: str = None, msg_id: str = None):
        super().__init__(value, msg_id, pattern='^[0-9a-zA-Z\-_\.+]+@[0-9a-zA-Z\-]+\.[a-z0-9]+$', ignore_case=True)


class DateTime(Base):
    """Date/time Rule.
    """

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        from datetime import datetime
        if isinstance(self._value, str):
            self._value = self._value.strip()

            try:
                self._value = _util.parse_rfc822_datetime_str(self._value)
            except ValueError:
                if self._value and not _re.match('\d{2}\.\d{2}\.\d{4} \d{2}\.\d{2}', self._value):
                    raise _error.RuleError(self._msg_id, self._msg_args)

        elif not isinstance(self._value, datetime):
            raise _error.RuleError(self._msg_id, self._msg_args)


class ListListItemNotEmpty(Base):
    def __init__(self, value: list = None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args)
        self._index = kwargs.get('sub_list_item_index', 0)

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if not isinstance(self.value, list):
            msg = _lang.t('pytsite.validation@list_expected', {'got': self.value.__class__.__name__})
            raise TypeError(msg)

        for row, sub_list in enumerate(self.value):
            if not isinstance(sub_list, list):
                msg = _lang.t('pytsite.validation@list_expected', {'got': self.value.__class__.__name__})
                raise TypeError(msg)

            if self._index + 1 > len(sub_list):
                raise _error.RuleError(self._msg_id, dict(self._msg_args, row=row + 1, col=self._index + 1))

            if not sub_list[self._index]:
                raise _error.RuleError(self._msg_id, dict(self._msg_args, row=row + 1, col=self._index + 1))


class ListListItemUrl(ListListItemNotEmpty):
    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if not isinstance(self.value, list):
            msg = _lang.t('pytsite.validation@list_expected', {'got': self.value.__class__.__name__})
            raise TypeError(msg)

        for row, sub_list in enumerate(self.value):
            if not isinstance(sub_list, list):
                msg = _lang.t('pytsite.validation@list_expected', {'got': self.value.__class__.__name__})
                raise TypeError(msg)

            if self._index + 1 > len(sub_list):
                raise _error.RuleError(self._msg_id, {'row': row + 1, 'col': self._index + 1})

            try:
                Url(sub_list[self._index], self._msg_id).validate()
            except _error.RuleError:
                raise _error.RuleError(self._msg_id, {'row': row + 1, 'col': self._index + 1})

"""PytSite Semver Version
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import SupportsInt as _SupportsInt
import re as _re
from . import _error

VERSION_PART_MAX = 99999

_VERSION_RE = _re.compile('^(\d+)(?:\.(\d+)(?:\.(\d+))?)?$')
_VERSION_RANGE_RE_V1 = _re.compile('(==|<=|>=|>|<|~|\^)\s*(\d+)(?:\.(\d+)(?:\.(\d+))?)?')
_VERSION_RANGE_RE_V2 = _re.compile('^(\d+|x|\*)(?:\.(\d+|x|\*)(?:\.(\d+|x|\*))?)?$')
_MAX_VERSION_STR = '{}.{}.{}'.format(VERSION_PART_MAX, VERSION_PART_MAX, VERSION_PART_MAX)

class Version(_SupportsInt):
    def __init__(self, version=0):
        """
        Init

        :param _Union[str, int, Version] version: version
        """
        self._major = self._minor = self._patch = 0

        if isinstance(version, Version):
            self._major = version.major
            self._minor = version.minor
            self._patch = version.patch
        elif isinstance(version, str):
            match = _VERSION_RE.findall(str(version))
            if not match:
                raise _error.InvalidVersionIdentifier(version)
            self.major, self.minor, self.patch = match[0][0], match[0][1], match[0][2]
        elif isinstance(version, int):
            version = '{:015d}'.format(version)
            self.major = version[:5].strip()
            self.minor = version[5:10].strip()
            self.patch = version[10:].strip()
        else:
            raise TypeError('Version identifier must be a str or Version instance, not {}'.format(type(version)))

    @property
    def major(self) -> int:
        return self._major

    @major.setter
    def major(self, value: int):
        value = int(value or 0)
        if value < 0 or value > VERSION_PART_MAX:
            raise ValueError('Major number must be between 0 and {}'.format(VERSION_PART_MAX))
        self._major = value

    @property
    def minor(self) -> int:
        return self._minor

    @minor.setter
    def minor(self, value: int):
        value = int(value or 0)
        if value < 0 or value > VERSION_PART_MAX:
            raise ValueError('Minor number must be between 0 and {}'.format(VERSION_PART_MAX))
        self._minor = value

    @property
    def patch(self) -> int:
        return self._patch

    @patch.setter
    def patch(self, value: int):
        value = int(value or 0)
        if value < 0 or value > VERSION_PART_MAX:
            raise ValueError('Patch number must be between 0 and {}'.format(VERSION_PART_MAX))
        self._patch = value

    def __str__(self) -> str:
        return '{}.{}.{}'.format(self._major, self._minor, self._patch)

    def __repr__(self) -> str:
        return "{}('{}')".format(self.__class__.__name__, str(self))

    def __hash__(self) -> int:
        return int(self)

    def __int__(self) -> int:
        return int('{:05d}{:05d}{:05d}'.format(self._major, self._minor, self._patch))

    def __lt__(self, other) -> bool:
        return int(self) < int(Version(other))

    def __le__(self, other) -> bool:
        return int(self) <= int(Version(other))

    def __gt__(self, other) -> bool:
        return int(self) > int(Version(other))

    def __ge__(self, other) -> bool:
        return int(self) >= int(Version(other))

    def __eq__(self, other) -> bool:
        return int(self) == int(Version(other))

    def __ne__(self, other) -> bool:
        return int(self) != int(Version(other))

    def __add__(self, other):
        return Version(int(self) + int(other))

    def __sub__(self, other):
        return Version(int(self) - int(other))


class VersionRange:
    def __init__(self, v_range=None):
        """
        :param _Union[str, VersionRange] v_range: version range
        """
        self._minimum = Version('0.0.0')
        self._maximum = Version('{}.{}.{}'.format(VERSION_PART_MAX, VERSION_PART_MAX, VERSION_PART_MAX))

        if not v_range or v_range in ('*', 'x'):
            return

        if isinstance(v_range, str):
            match = _VERSION_RANGE_RE_V1.findall(v_range)
            if match:
                for m in match:
                    op = m[0]
                    if op in ('>', '>='):
                        self._minimum.major = m[1]
                        self._minimum.minor = m[2] or 0
                        self._minimum.patch = m[3] or 0
                        if op == '>':
                            self._minimum += 1
                    elif op in ('<', '<='):
                        self._maximum.major = m[1]
                        self._maximum.minor = m[2] or 0
                        self._maximum.patch = m[3] or 0
                        if op == '<':
                            self._maximum -= 1
                    elif op == '==':
                        if m[1]:
                            self._minimum.major = self._maximum.major = m[1]
                        if m[2]:
                            self._minimum.minor = self._maximum.minor = m[2]
                        if m[3]:
                            self._minimum.patch = self._maximum.patch = m[3] or 0
                    elif op == '^':
                        self._minimum.major = self._maximum.major = m[1]
                        self._minimum.minor = m[2] or 0
                        self._minimum.patch = m[3] or 0
                    elif op == '~':
                        self._minimum.major = self._maximum.major = m[1]
                        self._minimum.minor = self._maximum.minor = m[2] or 0
                        self._minimum.patch = m[3] or 0

                if self._minimum > self._maximum:
                    raise _error.InvalidVersionRangeIdentifier(v_range)

            else:
                match = _VERSION_RANGE_RE_V2.findall(v_range)
                if match:
                    for i in range(3):
                        if match[0][i] in ('', 'x', '*'):
                            if i == 0:
                                self._minimum.major = 0
                                self._maximum.major = VERSION_PART_MAX
                            elif i == 1:
                                self._minimum.minor = 0
                                self._maximum.minor = VERSION_PART_MAX
                            elif i == 2:
                                self._minimum.patch = 0
                                self._maximum.patch = VERSION_PART_MAX
                        else:
                            if i == 0:
                                self._minimum.major = match[0][i]
                                self._maximum.major = match[0][i]
                            elif i == 1:
                                self._minimum.minor = match[0][i]
                                self._maximum.minor = match[0][i]
                            elif i == 2:
                                self._minimum.patch = match[0][i]
                                self._maximum.patch = match[0][i]
                else:
                    raise _error.InvalidVersionRangeIdentifier(v_range)

        elif isinstance(v_range, VersionRange):
            self._minimum = v_range.minimum
            self._maximum = v_range.maximum

        else:
            raise TypeError(
                'Version range identifier must be a str or VersionRange instance, got {}'.format(type(v_range)))

    @property
    def minimum(self) -> Version:
        return self._minimum

    @property
    def maximum(self) -> Version:
        return self._maximum

    def __contains__(self, item):
        if isinstance(item, (list, tuple)):
            for i in item:
                if i in self:
                    return True
            return False

        if isinstance(item, str):
            item = Version(item)

        if isinstance(item, Version):
            return self.minimum <= item <= self.maximum

        if isinstance(item, VersionRange):
            return self.minimum <= item.minimum and self.maximum >= item.maximum

    def __str__(self) -> str:
        # Exact version
        if self._minimum == self._maximum:
            return '=={}'.format(self._minimum)

        # Greater or equals version
        elif self._maximum == _MAX_VERSION_STR:
            return '>={}'.format(self._minimum)

        # Fixed major version
        elif self._minimum.major == self._maximum.major:
            # Fixed minor version
            if self._minimum.minor == self._maximum.minor:
                # Any patch version
                if self._minimum.patch == 0 and self._maximum.patch == VERSION_PART_MAX:
                    return '=={}.{}.*'.format(self._minimum.major, self._minimum.minor)

            # Any minor version
            elif self._minimum.minor == 0 and self._maximum.minor == VERSION_PART_MAX:
                # Any patch version
                if self._minimum.patch == 0 and self._maximum.patch == VERSION_PART_MAX:
                    return '=={}.*'.format(self._minimum.major, self._minimum.minor)

        return '>={},<={}'.format(self._minimum, self._maximum)

    def __repr__(self) -> str:
        return "{}('{}')".format(self.__class__.__name__, str(self))

    def __int__(self) -> int:
        return int(self._minimum) + int(self.maximum)

    def __hash__(self) -> int:
        return int(self)

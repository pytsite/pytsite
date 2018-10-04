"""PytSite Semver Version
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import SupportsInt as _SupportsInt, List as _List, Union as _Union
import re as _re
from . import _error

_VERSION_RE = _re.compile('^(\d+)(?:\.(\d+)(?:\.(\d+))?)?$')
_VERSION_RANGE_RE_V1 = _re.compile('(==|<=|>=|>|<)\s*(\d+)(?:\.(\d+)(?:\.(\d+))?)?')
_VERSION_RANGE_RE_V2 = _re.compile('^(\d+|x|\*)(?:\.(\d+|x|\*)(?:\.(\d+|x|\*))?)?$')


class Version(_SupportsInt):
    def __init__(self, version):
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
            if version >= 10000:
                self.major = int(version / 10000)
                version -= self.major * 10000
            if version >= 100:
                self.minor = int(version / 100)
                version -= self.minor * 100
            if version < 100:
                self.patch = version
        else:
            raise TypeError('Version identifier must be a str, int or Version instance, got {}'.format(type(version)))

    @property
    def major(self) -> int:
        return self._major

    @major.setter
    def major(self, value: int):
        value = int(value or 0)
        if not 0 <= value <= 99:
            raise ValueError('Major number must be between 0 and 99')

        self._major = value

    @property
    def minor(self) -> int:
        return self._minor

    @minor.setter
    def minor(self, value: int):
        value = int(value or 0)
        if not 0 <= value <= 99:
            raise ValueError('Minor number must be between 0 and 99')

        self._minor = value

    @property
    def patch(self) -> int:
        return self._patch

    @patch.setter
    def patch(self, value: int):
        value = int(value or 0)
        if not 0 <= value <= 99:
            raise ValueError('Patch number must be between 0 and 99')

        self._patch = value

    def __int__(self) -> int:
        return (self._major * 10000) + (self._minor * 100) + self._patch

    def __str__(self) -> str:
        return '{}.{}.{}'.format(self._major, self._minor, self._patch)

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

    def __add__(self, other: int):
        if not isinstance(other, int):
            raise TypeError('Only integers can be added to version')

        return Version(int(self) + other)

    def __sub__(self, other: int):
        if not isinstance(other, int):
            raise TypeError('Only integers can be subtracted from version')

        return Version(int(self) - other)


class VersionRange:
    def __init__(self, v_range):
        """
        :param _Union[str, VersionRange] v_range: version range
        """
        self._minimum = Version('0')
        self._maximum = Version('99.99.99')

        if isinstance(v_range, str):
            match = _VERSION_RANGE_RE_V1.findall(v_range)
            if match:
                for m in match:
                    op = m[0]
                    if op in ('>', '>='):
                        self._minimum.major = int(m[1])
                        self._minimum.minor = int(m[2] or 0)
                        self._minimum.patch = int(m[3] or 0)
                        if op == '>':
                            self._minimum += 1
                    elif op in ('<', '<='):
                        self._maximum.major = int(m[1])
                        self._maximum.minor = int(m[2] or 0)
                        self._maximum.patch = int(m[3] or 0)
                        if op == '<':
                            self._maximum -= 1
                    elif op == '==':
                        self._minimum.major = self._maximum.major = int(m[1])
                        self._minimum.minor = self._maximum.minor = int(m[2])
                        self._minimum.patch = self._maximum.patch = int(m[3])

                if self._minimum > self._maximum:
                    raise _error.InvalidVersionRangeIdentifier(v_range)

            else:
                match = _VERSION_RANGE_RE_V2.findall(v_range)
                if match:
                    for i in range(3):
                        if match[0][i] in ('', 'x', '*'):
                            if i == 0:
                                self._minimum.major = 0
                                self._maximum.major = 99
                            elif i == 1:
                                self._minimum.minor = 0
                                self._maximum.minor = 99
                            elif i == 2:
                                self._minimum.patch = 0
                                self._maximum.patch = 99
                        else:
                            if i == 0:
                                self._minimum.major = int(match[0][i])
                                self._maximum.major = int(match[0][i])
                            elif i == 1:
                                self._minimum.minor = int(match[0][i])
                                self._maximum.minor = int(match[0][i])
                            elif i == 2:
                                self._minimum.patch = int(match[0][i])
                                self._maximum.patch = int(match[0][i])
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

    def __str__(self) -> str:
        return '>={} <={}'.format(self._minimum, self._maximum)

"""PytSite Semver Version
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import SupportsInt as _SupportsInt, List as _List, Union as _Union
from . import _error


class Version(_SupportsInt):
    @staticmethod
    def _from_int(version: int) -> tuple:
        major = minor = 0

        if version >= 10000:
            major = int(version / 10000)
            version -= major * 10000

        if version >= 100:
            minor = int(version / 100)
            version -= minor * 100

        return major, minor, version

    @staticmethod
    def _normalize(version: _Union[str, int, list, tuple]) -> _List[int]:
        if isinstance(version, str):
            try:
                v_list = [int(v) for v in version.replace(' ', '').split('.')]
            except ValueError:
                raise _error.InvalidVersionString("Invalid version string: '{}'.".format(version))
        elif isinstance(version, int):
            v_list = list(Version._from_int(version))
        else:
            v_list = list(version)

        v_len = len(v_list)
        if v_len == 1:
            v_list.extend([0, 0])
        elif v_len == 2:
            v_list.append(0)
        elif v_len > 3:
            v_list = v_list[:3]

        return v_list

    def __init__(self, version: _Union[str, int, list, tuple]):
        self._major = self._minor = self._patch = 0
        self.update(version)

    def update(self, version: _Union[str, int, list, tuple]):
        self.major, self.minor, self.patch = self._normalize(version)

    @property
    def major(self) -> int:
        return self._major

    @major.setter
    def major(self, value: int):
        value = int(value)
        if not 0 <= value <= 99:
            raise ValueError('Major number should be between 0 and 99')

        self._major = value

    @property
    def minor(self) -> int:
        return self._minor

    @minor.setter
    def minor(self, value: int):
        value = int(value)
        if not 0 <= value <= 99:
            raise ValueError('Minor number should be between 0 and 99')

        self._minor = value

    @property
    def patch(self) -> int:
        return self._patch

    @patch.setter
    def patch(self, value: int):
        value = int(value)
        if not 0 <= value <= 99:
            raise ValueError('Patch number should be between 0 and 99')

        self._patch = value

    def __int__(self) -> int:
        return (self._major * 10000) + (self._minor * 100) + self._patch

    def __str__(self) -> str:
        return '{}.{}.{}'.format(self._major, self._minor, self._patch)

    def __lt__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) < int(other)

    def __le__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) <= int(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) > int(other)

    def __ge__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) >= int(other)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) == int(other)

    def __ne__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) != int(other)

    def __add__(self, other: int):
        if not isinstance(other, int):
            raise TypeError('Only integers can be added to version')

        return Version(int(self) + other)

    def __sub__(self, other: int):
        if not isinstance(other, int):
            raise TypeError('Only integers can be subtracted from version')

        return Version(int(self) - other)

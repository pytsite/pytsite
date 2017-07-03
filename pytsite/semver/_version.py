"""PytSite Semver Version
"""
from typing import SupportsInt as _SupportsInt
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Version(_SupportsInt):
    def __init__(self, version: str):
        self._str_representation = self._normalize(version)

        vs = self._str_representation.split('.')
        self._int_representation = (int(vs[0]) * 1000000) + (int(vs[1]) * 1000) + int(vs[2])

    @staticmethod
    def _normalize(version: str) -> str:
        v_list = version.replace(' ', '').split('.')
        v_len = len(v_list)

        if v_len == 1:
            v_list.extend(['0', '0'])
        elif v_len == 2:
            v_list.append('0')
        elif v_len > 3:
            raise _error.InvalidVersionString("Invalid version string: '{}'.".format(version))

        for v_part in v_list:
            if not v_part.isdigit():
                raise _error.InvalidVersionString("Invalid version string: '{}'.".format(version))

        return '.'.join(v[:3] for v in v_list)

    def __int__(self) -> int:
        return self._int_representation

    def __str__(self) -> str:
        return self._str_representation

    def __lt__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) < int(other)

    def __gt__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) > int(other)

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            other = Version(other)

        return int(self) == int(other)

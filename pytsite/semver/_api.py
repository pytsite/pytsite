"""PytSite Semantic Versioning Tools Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from typing import Optional as _Optional, Union as _Union, Iterable as _Iterable
from ._version import Version as _Version, VersionRange as _VersionRange

_REQUIREMENT_RE = _re.compile('^([a-zA-Z\-_0-9]+)(?:\s*(.+)?)?$')


def _to_int(version: str) -> int:
    """Get integer representation of version string
    """
    return int(_Version(version))


def last(versions: _Iterable[str], constraints: _Union[str, _Iterable[str]] = None) -> _Optional[str]:
    """Get latest version from list of versions
    """
    if not versions:
        return None

    versions = sorted(versions, key=_to_int)

    # Return latest available
    if not constraints:
        return versions[-1]

    # Search for latest available among constraints
    filtered = []
    for v in versions:
        if v in constraints:
            filtered.append(v)

    return filtered[-1] if filtered else None

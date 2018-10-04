"""PytSite Semantic Versioning Tools Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from typing import Optional as _Optional, Union as _Union, Iterable as _Iterable, Tuple as _Tuple
from . import _error
from ._version import Version as _Version, VersionRange as _VersionRange

_REQUIREMENT_RE = _re.compile('^([a-zA-Z\-_0-9]+)(?:\s*(.+)?)?$')


def parse_requirement_str(requirement: str) -> _Tuple[str, _VersionRange]:
    """Parse a requirement string

    Requirement string is a string contains two parts: name and version range, i. e.:
    'pytsite >1.1 <2.0', 'wsgi==1.2.1', 'python 3.x' and so on.
    """
    match = _REQUIREMENT_RE.findall(requirement)
    if not match:
        raise _error.InvalidRequirementString("'{}' is not a valid requirement string".format(requirement))

    return match[0][0], _VersionRange(match[0][1] or '*')


def parse_version_str(version: str) -> _Version:
    """Parse version string
    """
    return _Version(version)


def compare(a: _Union[str, _Version], b: _Union[str, _Version]) -> int:
    """Compare two versions

    Returns -1 if a < b, 0 if a == b, 1 if a > b
    """

    if not isinstance(a, _Version):
        a = _Version(a)

    if not isinstance(b, _Version):
        b = _Version(b)

    if a < b:
        return -1
    elif a > b:
        return 1
    else:
        return 0


def to_int(version: str) -> int:
    """Get integer representation of version string
    """
    return int(_Version(version))


def last(versions: _Iterable[str], conditions: _Union[str, _Iterable[str]] = None) -> _Optional[str]:
    """Get latest version from list of versions
    """
    if not versions:
        return None

    versions = sorted(versions, key=to_int)

    # Return latest available
    if not conditions:
        return versions[-1]

    # Search for latest available among conditions
    filtered = []
    for v in versions:
        if check_conditions(v, conditions):
            filtered.append(v)

    return filtered[-1] if filtered else None


def check_conditions(v_to_check: _Union[str, _Version],
                     v_range: _Union[str, _Iterable[str], _VersionRange, _Iterable[_VersionRange]]) -> bool:
    """Check if version_to_check satisfies condition

    version_to_check should be like '1', '1.0' or '1.0.0'.
    condition should be like '==1', '>=1.0', '!=1.0.0', etc.
    """
    if isinstance(v_range, (list, tuple)):
        r = True
        for c in v_range:
            r = check_conditions(v_to_check, c)
            if not r:
                return r
        return r

    v_range = _VersionRange(v_range)

    return v_range.minimum <= _Version(v_to_check) <= v_range.maximum

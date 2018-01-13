"""PytSite Semantic Versioning Tools Functions
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
from typing import Optional as _Optional, Union as _Union, Iterable as _Iterable, Tuple as _Tuple
from . import _error
from ._version import Version as _Version

_REQUIREMENT_RE = _re.compile('([a-zA-Z0-9_.\-]+)\s*(==|!=|<=|>=|>|<)?\s*(\d+\.\d+\.\d+|\d+\.\d+|\d+)?')
_CONDITION_RE = _re.compile('^(==|!=|<=|>=|>|<)?([0-9.]+)$')


def parse_condition_str(condition: str) -> _Tuple[str, _Version]:
    """Parse a condition string

    Condition string must consist of two parts: a comparison operator and a version number,
    i. e. '>=0.0.1', '<3.2.1', etc.
    """
    match = _CONDITION_RE.match(condition.replace(' ', ''))

    if not match:
        raise _error.InvalidCondition("Invalid condition string: '{}'".format(condition))

    operator = match.group(1) or '=='
    version = match.group(2)

    return operator, _Version(version)


def parse_requirement_str(requirement: str) -> _Tuple[str, str]:
    """Parse a requirement string

    Requirement string is a string contains three parts: name, condition and version, i. e.: 'pytsite > 1.1' or
    'wsgi == 1.2.1' and so on.

    If condition and version is not specified, condition will be considered as '>=' and version -- as '0.0.1'.

    Returns tuple of 2 elements: name and condition, i. e. ('pytsite', '>1.1') or ('wsgi', '>=1.2.1')
    """
    match = _REQUIREMENT_RE.match(requirement)
    if not match:
        raise _error.InvalidRequirementString("'{}' is not a valid requirement string".format(requirement))

    name, condition, version = match.group(1), match.group(2), match.group(3)

    return name, '{}{}'.format(condition or '>=', str(_Version(version)) if version else '0.0.1')


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


def increment(version: str) -> str:
    """Increment a version by one
    """
    return str(_Version(version) + 1)


def decrement(version: str) -> str:
    """Decrement a version by one
    """
    return str(_Version(version) - 1)


def to_int(version: str) -> int:
    """Get integer representation of version string
    """
    return int(_Version(version))


def minimum(condition: str) -> str:
    """Get minimum possible version number for provided condition
    """
    op, ver = parse_condition_str(condition)

    if op == '>':
        return str(ver + 1)
    elif op.startswith('<'):
        ver = '0.0.0'

    return str(ver)


def maximum(condition: str) -> str:
    """Get maximum possible version number for provided condition
    """
    op, ver = parse_condition_str(condition)

    if op == '<':
        return str(ver - 1)
    elif op.startswith('>'):
        ver = '99.99.99'

    return str(ver)


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


def check_conditions(version_to_check: _Union[str, _Version], conditions: _Union[str, _Iterable[str]]) -> bool:
    """Check if version_to_check satisfies condition

    version_to_check should be like '1', '1.0' or '1.0.0'.
    condition should be like '==1', '>=1.0', '!=1.0.0', etc.
    """
    if isinstance(conditions, (list, tuple)):
        r = True
        for c in conditions:
            r = check_conditions(version_to_check, c)
            if not r:
                return r
        return r

    operator, version_to_compare = parse_condition_str(conditions)

    if operator == '==':
        if compare(version_to_check, version_to_compare) != 0:
            return False
    elif operator == '!=':
        if compare(version_to_check, version_to_compare) == 0:
            return False
    elif operator == '<':
        if compare(version_to_check, version_to_compare) >= 0:
            return False
    elif operator == '>':
        if compare(version_to_check, version_to_compare) <= 0:
            return False
    elif operator == '<=':
        if compare(version_to_check, version_to_compare) > 0:
            return False
    elif operator == '>=':
        if compare(version_to_check, version_to_compare) < 0:
            return False

    return True

"""PytSite Semantic Versioning Tools Functions
"""
import re as _re
from typing import Optional as _Optional, List as _List
from . import _error
from ._version import Version as _Version

_CONDITION_RE = _re.compile('^([<>=!]{1,2})?([0-9\.]+)$')
_ALLOWED_OPERATORS = ('==', '!=', '>', '<', '>=', '<=')

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _parse_condition(condition: str) -> tuple:
    match = _CONDITION_RE.match(condition.replace(' ', ''))

    if not match:
        raise _error.InvalidCondition("Invalid condition string: '{}'".format(condition))

    operator = match.group(1) or '=='
    version = match.group(2)

    if operator not in _ALLOWED_OPERATORS:
        raise _error.InvalidComparisonOperator("Unknown comparison operator '{}' used in condition '{}'".
                                               format(operator, version))

    return operator, version


def parse(version: str) -> _Version:
    """Parse version string
    """
    return _Version(version)


def compare(a: str, b: str) -> int:
    """Compare two versions

    Returns -1 if a < b, 0 if a == b, 1 if a > b
    """

    a = _Version(a)
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


def latest(versions: _List[str]) -> _Optional[str]:
    """Get latest version from list of versions
    """
    try:
        return sorted(versions, key=to_int)[-1]
    except IndexError:
        return None


def check_condition(version_to_check: str, condition: str) -> bool:
    """Check if version_to_check satisfies condition

    version_to_check should be like '1', '1.0' or '1.0.0'.
    condition should be like '==1', '>=1.0', '!=1.0.0', etc.
    """

    operator, version_to_comapre = _parse_condition(condition)

    if operator == '==':
        if compare(version_to_check, version_to_comapre) != 0:
            return False
    elif operator == '!=':
        if compare(version_to_check, version_to_comapre) == 0:
            return False
    elif operator == '<':
        if compare(version_to_check, version_to_comapre) >= 0:
            return False
    elif operator == '>':
        if compare(version_to_check, version_to_comapre) <= 0:
            return False
    elif operator == '<=':
        if compare(version_to_check, version_to_comapre) > 0:
            return False
    elif operator == '>=':
        if compare(version_to_check, version_to_comapre) < 0:
            return False

    return True

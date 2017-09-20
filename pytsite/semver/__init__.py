"""PytSite Semantic Versioning Tools

http://semver.org/
"""

# Public API
from . import _error as error
from ._api import parse_version_str, compare, last, check_conditions, to_int, parse_requirement_str, \
    parse_condition_str, minimum, maximum, increment, decrement
from ._version import Version

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

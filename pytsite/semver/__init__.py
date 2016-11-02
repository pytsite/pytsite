"""PytSite Semantic Versioning Tools.

http://semver.org/
"""

# Public API
from . import _error as error
from ._api import normalize, compare, latest

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

"""PytSite Semantic Versioning Tools

http://semver.org/
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._api import last
from ._version import Version, VersionRange

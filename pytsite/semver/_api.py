"""PytSite Semantic Versioning Tools Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import Optional as _Optional, Iterable as _Iterable
from ._version import Version as _Version, VersionRange as _VersionRange


def last(versions: _Iterable[_Version], v_range: _VersionRange = None) -> _Optional[_Version]:
    """Get latest available version from list of versions
    """
    if not versions:
        return None

    versions = sorted(versions, key=int)

    # Return latest available
    if not v_range:
        return versions[-1]

    # Search for latest available among constraints
    filtered = [v for v in versions if v in v_range]

    return filtered[-1] if filtered else None

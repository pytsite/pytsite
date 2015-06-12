"""Geo Validation Rules.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.validation.rules import DictValueNotEmptyRule


class GeoAddressNotEmptyRule(DictValueNotEmptyRule):
    """Check if an address structure is empty.
    """

    def __init__(self, msg_id: str=None, value=None):
        """Init.
        """
        if not msg_id:
            msg_id = 'pytsite.geo@validation_geoaddressnotemptyrule'
        super().__init__(msg_id, value)
        self._keys = ('address', 'name', 'lat', 'lng')

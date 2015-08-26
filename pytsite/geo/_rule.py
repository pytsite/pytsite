"""Geo Validation Rules
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import validation as _validation


class AddressNotEmpty(_validation.rule.DictPartsNotEmpty):
    """Check if an address structure is empty.
    """
    def __init__(self, msg_id: str=None, value=None):
        """Init.
        """
        if not msg_id:
            msg_id = 'pytsite.geo@validation_geoaddressnotempty'

        super().__init__(msg_id, value)

        self._keys = ('address', 'lng_lat', 'components')

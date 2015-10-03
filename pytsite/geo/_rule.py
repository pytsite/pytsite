"""Geo Validation Rules
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import validation as _validation


class AddressNotEmpty(_validation.rule.DictPartsNotEmpty):
    """Check if an address structure is empty.
    """
    def __init__(self, value=None, msg_id: str=None):
        """Init.
        """
        if not msg_id:
            msg_id = 'pytsite.geo@validation_geoaddressnotempty'

        super().__init__(value, msg_id, ('address', 'lng_lat', 'components'))

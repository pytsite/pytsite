"""Geo ODM Fields.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import odm as _odm


class Location(_odm.field.Dict):
    """Geo Location Field.
    """
    def set_val(self, value: dict, change_modified: bool=True, **kwargs):
        """Hook.
        """
        return super().set_val(value, change_modified, **kwargs)

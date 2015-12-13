"""PytSite ODM Init Tests.
"""
from pytsite import odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestInit:
    def test_init(self):
        # Modules
        assert hasattr(odm, 'field')
        assert hasattr(odm, 'validation')
        assert hasattr(odm, 'error')

        # Constants
        assert hasattr(odm, 'I_ASC')
        assert hasattr(odm, 'I_DESC')
        assert hasattr(odm, 'I_TEXT')
        assert hasattr(odm, 'I_GEO2D')

        # Classes
        assert hasattr(odm, 'Model')
        assert hasattr(odm, 'Finder')
        assert hasattr(odm, 'FinderResult')

        # Functions
        assert hasattr(odm, 'register_model')
        assert hasattr(odm, 'unregister_model')
        assert hasattr(odm, 'is_model_registered')
        assert hasattr(odm, 'dispense')
        assert hasattr(odm, 'cache_get')
        assert hasattr(odm, 'cache_put')
        assert hasattr(odm, 'cache_delete')
        assert hasattr(odm, 'get_by_ref')
        assert hasattr(odm, 'resolve_ref')

        assert hasattr(odm, 'get_model_class')
        assert hasattr(odm, 'find')

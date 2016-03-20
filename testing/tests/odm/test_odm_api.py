"""PytSite ODM API Functions Tests.
"""
import pytest
from pytsite import odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class FixtureModel(odm.Entity):
    def _setup_fields(self):
        pass


class TestApi:
    def test_register_model(self):
        # Register with class object
        with pytest.raises(NameError):
            odm.register_model('fixture', UnknownClass)
        odm.register_model('fixture', FixtureModel)

        # Register with class string name
        odm.register_model('fixture', 'test_odm_api.FixtureModel', True)
        with pytest.raises(NameError):
            odm.register_model('fixture', 'UnknownClass', True)

        # Register with the same name
        odm.register_model('fixture', FixtureModel, True)
        with pytest.raises(odm.error.ModelAlreadyRegistered):
            odm.register_model('fixture', FixtureModel)

        # Cleanup
        odm.unregister_model('fixture')

    def test_unregister_model(self):
        odm.register_model('fixture', FixtureModel)
        odm.unregister_model('fixture')

        with pytest.raises(odm.error.ModelNotRegistered):
            odm.unregister_model('fixture')

    def test_is_model_registered(self):
        assert odm.is_model_registered('fixture') == False
        odm.register_model('fixture', FixtureModel)
        assert odm.is_model_registered('fixture') == True

        # Cleanup
        odm.unregister_model('fixture')

    def test_get_model_class(self):
        odm.register_model('fixture', FixtureModel)
        assert odm.get_model_class('fixture') == FixtureModel

        # Cleanup
        odm.unregister_model('fixture')

    def test_get_registered_models(self):
        assert isinstance(odm.get_registered_models(), tuple)
        assert 'fixture' not in odm.get_registered_models()

        odm.register_model('fixture', FixtureModel)
        assert 'fixture' in odm.get_registered_models()

        # Cleanup
        odm.unregister_model('fixture')
        assert 'fixture' not in odm.get_registered_models()

    def test_resolve_ref(self):
        odm.register_model('fixture', FixtureModel)
        entity = odm.dispense('fixture').save()

        assert odm.resolve_ref(None) is None
        assert odm.resolve_ref(entity.ref) == entity.ref
        assert odm.resolve_ref(entity) == entity.ref
        assert odm.resolve_ref(entity.model + ':' + str(entity.id)) == entity.ref

        with pytest.raises(ValueError):
            odm.resolve_ref('')
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            odm.resolve_ref([])
        with pytest.raises(odm.error.ModelNotRegistered):
            odm.resolve_ref('unknown_model:561c12f4523af50c3b41c3cc')

        # Cleanup
        entity.delete()
        odm.unregister_model('fixture')

    def test_get_by_ref(self):
        odm.register_model('fixture', FixtureModel)
        entity = odm.dispense('fixture').save()

        assert odm.get_by_ref(entity.ref) is entity
        assert odm.get_by_ref(entity.model + ':' + str(entity.id)) is entity

        # Cleanup
        entity.delete()
        odm.unregister_model('fixture')

    def test_dispense(self):
        odm.register_model('fixture', FixtureModel)

        entity = odm.dispense('fixture')
        with pytest.raises(odm.error.ModelNotRegistered):
            odm.dispense('unknown_model')

        assert isinstance(entity, FixtureModel)

        # Cleanup
        odm.unregister_model('fixture')

    def test_cache_get_put_delete(self):
        odm.register_model('fixture', FixtureModel)

        assert odm.cache_get('fixture', None) is None

        entity = odm.dispense('fixture')
        entity.save()

        # Entity is in the cache immediately after save
        assert odm.cache_get('fixture', entity.id) is entity

        odm.cache_delete(entity)
        assert odm.cache_get('fixture', entity.id) is None

        # Cleanup
        entity.delete()
        odm.unregister_model('fixture')

    def test_find(self):
        odm.register_model('fixture', FixtureModel)

        assert isinstance(odm.find('fixture'), odm.Finder)
        with pytest.raises(odm.error.ModelNotRegistered):
            odm.find('unknown_model')

        # Cleanup
        odm.unregister_model('fixture')

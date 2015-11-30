"""PytSite ODM Model Tests.
"""
import pytest
from collections import OrderedDict
from bson.objectid import ObjectId as BSONObjectId
from pymongo.collection import Collection
from pytsite import odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class FixtureModel(odm.Model):
    def _setup(self):
        self._define_field(odm.field.String('str_f'))


class TestModel:
    entity = None
    """:type: odm.Model"""

    @classmethod
    def setup_class(cls):
        odm.register_model('fixture', FixtureModel)
        cls.entity = odm.dispense('fixture').save()

    @classmethod
    def teardown_class(cls):
        cls.entity.delete()
        odm.unregister_model('fixture')

    def test_has_field(self):
        assert TestModel.entity.has_field('str_f') == True
        assert TestModel.entity.has_field('unknown_f') == False

    def get_field(self):
        assert isinstance(TestModel.entity.get_field('str_f'), odm.field.Abstract)
        with pytest.raises(odm.error.FieldNotDefined):
            TestModel.entity.get_field('unknown_f')

    def test_collection(self):
        assert isinstance(TestModel.entity.collection, Collection)

    def test_fields(self):
        fields = TestModel.entity.fields

        assert isinstance(fields, OrderedDict)
        assert len(fields) == 7
        assert isinstance(fields['_id'], odm.field.ObjectId)
        assert isinstance(fields['_model'], odm.field.String)
        assert isinstance(fields['_parent'], odm.field.Ref)
        assert isinstance(fields['_children'], odm.field.RefsList)
        assert isinstance(fields['_created'], odm.field.DateTime)
        assert isinstance(fields['_modified'], odm.field.DateTime)
        assert isinstance(fields['str_f'], odm.field.String)

    def test_id(self):
        assert isinstance(TestModel.entity.id, BSONObjectId)

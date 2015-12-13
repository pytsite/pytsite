"""PytSite ODM Model Tests.
"""
import pytest
from collections import OrderedDict
from bson.objectid import ObjectId as BSONObjectId
from bson.dbref import DBRef as BSONDBRef
from pymongo.collection import Collection
from pytsite import odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ModelOne(odm.Model):
    def _setup(self):
        self._define_field(odm.field.String('str_f'))


class ModelTwo(odm.Model):
    def _setup(self):
        self._define_field(odm.field.String('str_f'))


class TestModel:
    entity_m_one = None
    """:type: ModelOne"""

    entity_m_two = None
    """:type: ModelOne"""

    @classmethod
    def setup_class(cls):
        odm.register_model('model_one', ModelOne)
        odm.register_model('model_two', ModelTwo)
        cls.entity_m_one = odm.dispense('model_one').save()
        cls.entity_m_two = odm.dispense('model_two').save()

    @classmethod
    def teardown_class(cls):
        cls.entity_m_one.delete()
        cls.entity_m_two.delete()
        odm.unregister_model('model_one')
        odm.unregister_model('model_two')

    def test_has_field(self):
        assert TestModel.entity_m_one.has_field('str_f') == True
        assert TestModel.entity_m_one.has_field('unknown_f') == False

    def get_field(self):
        assert isinstance(TestModel.entity_m_one.get_field('str_f'), odm.field.Abstract)
        with pytest.raises(odm.error.FieldNotDefined):
            TestModel.entity_m_one.get_field('unknown_f')

    def test_collection(self):
        assert isinstance(TestModel.entity_m_one.collection, Collection)
        assert TestModel.entity_m_one.collection.name == 'model_ones'

    def test_fields(self):
        fields = TestModel.entity_m_one.fields

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
        assert isinstance(TestModel.entity_m_one.id, BSONObjectId)

    def test_ref(self):
        assert isinstance(TestModel.entity_m_one.ref, BSONDBRef)
        assert TestModel.entity_m_one.ref.collection == TestModel.entity_m_one.collection.name
        assert TestModel.entity_m_one.ref.id is TestModel.entity_m_one.id

    def test_append_child(self):
        # Setup
        one_1 = odm.dispense('model_one')
        one_2 = odm.dispense('model_one')

        # Check initial state
        assert len(one_1.children) == 0
        assert one_2.parent is None

        # Try to append unsaved child to unsaved parent
        with pytest.raises(odm.error.EntityNotStored):
            one_1.append_child(one_2)

        # Try to append saved child to unsaved parent
        one_2.save()
        one_2_id = str(one_2.id)
        with pytest.raises(odm.error.EntityNotStored):
            one_1.append_child(one_2)

        # Append saved child to saved parent
        one_1.save()
        one_1_id = str(one_1.id)
        one_1.append_child(one_2)

        # Checking references
        assert len(one_1.children) == 1
        assert one_1.children[0] is one_2
        assert one_2.parent is one_1

        # Cleanup
        one_1.delete()
        one_2.delete()

        # Test of appending child of different model
        one = odm.dispense('model_one')
        two = odm.dispense('model_two')
        with pytest.raises(TypeError):
            one.append_child(two)

        # Cleanup
        one.delete()
        two.delete()

    def test_remove_child(self):
        # Setup
        one_1 = odm.dispense('model_one').save()
        one_2 = odm.dispense('model_one').save()
        one_3 = odm.dispense('model_one').save()

        # Append children
        one_1.append_child(one_2)
        one_1.append_child(one_3)

        # Checking references
        assert len(one_1.children) == 2
        assert one_1.children[0] is one_2
        assert one_1.children[1] is one_3
        assert one_2.parent is one_1
        assert one_3.parent is one_1

        # Remove first child
        one_1.remove_child(one_2)
        assert len(one_1.children) == 1
        assert one_1.children[0] is one_3
        assert one_2.parent is None
        assert one_3.parent is one_1

        # Remove second child
        one_1.remove_child(one_3)
        assert len(one_1.children) == 0
        assert one_2.parent is None
        assert one_3.parent is None

        # Cleanup
        one_1.delete()
        one_2.delete()
        one_3.delete()

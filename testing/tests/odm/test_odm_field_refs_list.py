"""Description.
"""
import pytest
from pytsite import odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ModelOne(odm.Entity):
    def _setup_fields(self):
        self.define_field(odm.field.RefsList('refs', model='model_two'))


class ModelTwo(odm.Entity):
    def _setup_fields(self):
        self.define_field(odm.field.String('str'))


class TestFieldRefsList:
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

    def test_f_add(self):
        assert self.entity_m_one.f_get('refs') == ()

        self.entity_m_one.f_add('refs', self.entity_m_two).save()
        assert self.entity_m_one.f_get('refs') == (self.entity_m_two,)
        assert self.entity_m_one.f_get('refs')[0].id == self.entity_m_two.id

        self.entity_m_one.reload()
        assert self.entity_m_one.f_get('refs') == (self.entity_m_two,)
        assert self.entity_m_one.f_get('refs')[0].id == self.entity_m_two.id

        self.entity_m_one.f_sub('refs', self.entity_m_two).save()
        assert self.entity_m_one.f_get('refs') == ()
        self.entity_m_one.reload()
        assert self.entity_m_one.f_get('refs') == ()

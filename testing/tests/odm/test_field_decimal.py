"""ODM Decimal Field Tests.
"""
import decimal
import pytest
from pytsite import odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class TestFieldDecimal:
    def test_init(self):
        assert odm.field.Decimal('t').get_val() == decimal.Decimal(0)
        assert odm.field.Decimal('t', default=3.14).get_val() == decimal.Decimal('3.14')
        assert odm.field.Decimal('t', default=3.14).get_val() != decimal.Decimal(3.14)

    def test_get_val(self):
        f = odm.field.Decimal('t', default=1.234)
        assert isinstance(f.get_val(), decimal.Decimal)
        assert f.get_val() == decimal.Decimal('1.234')
        assert f.get_val() != decimal.Decimal(1.234)

    def test_get_storable_val(self):
        f = odm.field.Decimal('t', default=1.234)
        assert isinstance(f.get_storable_val(), float)
        assert f.get_storable_val() == 1.234

    def test_set_val(self):
        f = odm.field.Decimal('t')

        assert f.get_val() == decimal.Decimal(0)
        f.set_val(1.234)
        assert f.get_val() == decimal.Decimal('1.234')
        assert f.get_val() != decimal.Decimal(1.234)

    def test_clr_val(self):
        f = odm.field.Decimal('t', default=3.14)
        f.set_val(4.13)
        assert f.get_val() == decimal.Decimal('4.13')
        f.clr_val()
        assert f.get_val() == decimal.Decimal('3.14')

    def test_add_val(self):
        f = odm.field.Decimal('t')
        f.add_val(1.1)
        assert f.get_val() == decimal.Decimal('1.1')

    def test_sub_val(self):
        f = odm.field.Decimal('t', default=1.1)
        f.sub_val(2.2)
        assert f.get_val() == decimal.Decimal('-1.1')
        assert f.get_val() != decimal.Decimal(-1.1)

    def test_inc_val(self):
        with pytest.raises(ArithmeticError):
            odm.field.Decimal('t').inc_val()

    def test_dec_val(self):
        with pytest.raises(ArithmeticError):
            odm.field.Decimal('t').dec_val()

    def test_str_val(self):
        assert str(odm.field.Decimal('t', default=1.1).get_val()) == '1.1'

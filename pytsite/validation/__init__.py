"""Pytsite Validation Package
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _validator as validator, _rule as rule, _error as error
from ._validator import Validator
from ._rule import Rule
from ._error import RuleError, ValidatorError


def _init():
    from pytsite import lang
    lang.register_package(__name__)


_init()

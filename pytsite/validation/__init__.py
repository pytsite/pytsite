"""Pytsite Validation Package.
"""
# Public API
from . import _validator, _rule, _error

rule = _rule
error = _error
Validator = _validator.Validator
ValidatorError = _error.ValidatorError
RuleError = _error.RuleError

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import lang
    lang.register_package(__name__)


__init()

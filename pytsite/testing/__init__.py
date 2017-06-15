"""PytSite Testing Package
"""
from ._test_case import TestCase

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, console
    from . import _console_command

    lang.register_package(__name__)
    console.register_command(_console_command.Test())


_init()

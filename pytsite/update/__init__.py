"""PytSite Update
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import on_update_stage_1, on_update_stage_2, on_update_pytsite, on_update_app, on_update


def _init():
    """Init wrapper
    """
    from pytsite import console, lang
    from . import _cc

    lang.register_package(__name__)
    console.register_command(_cc.Update())


_init()

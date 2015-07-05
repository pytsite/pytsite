"""Poster Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Dependencies
__import__('pytsite.oauth')
__import__('pytsite.content')


def __init():
    from pytsite import admin
    from pytsite.core import router, odm, lang
    from ._model import Poster

    lang.register_package(__name__)
    odm.register_model('poster', Poster)

    admin.sidebar.add_menu('misc', 'posters', 'pytsite.poster@posters',
                           href=router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'poster'}),
                           icon='fa fa-bullhorn',
                           permissions=(
                               'pytsite.odm_ui.browse.poster',
                               'pytsite.odm_ui.browse_own.poster'
                           ))

__init()


# Public API
from ._driver import Abstract as AbstractDriver
from ._functions import register_driver

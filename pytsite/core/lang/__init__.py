"""Lang Plugin Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import events, console
from . import _commands
from ._functions import t, t_plural, register_package, define_languages, get_packages, get_langs, load_lang_file,\
    get_current_lang, set_current_lang, is_package_registered, get_lang_title

register_package(__name__, 'translations')

console.register_command(_commands.CompileTranslations())

def __router_dispatch():
    from pytsite.core import assetman
    assetman.add('app@js/translations.js')

events.listen('router.dispatch', __router_dispatch)
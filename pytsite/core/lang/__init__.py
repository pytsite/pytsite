"""Lang Plugin Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    from pytsite.core import console
    from . import _commands, _functions
    _functions.register_package(__name__, 'translations')
    console.register_command(_commands.CompileTranslations())

__init()

# Public API
from . import _error as error
from ._functions import t, t_plural, register_package, define_languages, get_packages, get_langs, load_lang_file,\
    get_current_lang, set_current_lang, is_package_registered, get_lang_title, time_ago, pretty_date

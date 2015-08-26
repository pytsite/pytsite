"""Lang Plugin Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._functions import t, t_plural, register_package, define_languages, get_packages, get_langs, load_lang_file,\
    get_current_lang, set_current_lang, is_package_registered, get_lang_title, time_ago, pretty_date, pretty_date_time

# Registering itself
register_package(__name__)

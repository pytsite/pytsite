"""Lang Plugin Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._functions import t, t_plural, register_package, define, get_packages, langs, load_lang_file,\
    get_current, set_current, is_package_registered, lang_title, time_ago, pretty_date, pretty_date_time

# Registering itself
register_package(__name__)

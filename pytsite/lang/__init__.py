"""pytsite.lang Init
"""
# Public API
from . import _error as error
from ._api import t, t_plural, register_package, define, get_packages, langs, load_lang_file, \
    get_current, set_current, is_package_registered, lang_title, time_ago, pretty_date, pretty_date_time, \
    is_translation_defined, get_fallback, set_fallback, ietf_tag, get_primary

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Registering itself
register_package(__name__)

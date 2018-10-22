"""PytSite Language Package
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from . import _error as error
from ._api import t, t_plural, register_package, define, is_defined, get_packages, langs, get_package_translations, \
    get_current, set_current, is_package_registered, lang_title, time_ago, pretty_date, pretty_date_time, \
    is_translation_defined, get_fallback, set_fallback, ietf_tag, get_primary, register_global, on_translate, \
    clear_cache, on_split_msg_id


def _init():
    from pytsite import reg, package_info

    def get_app_name(language: str, args: dict):
        return reg.get('app.app_name_' + language) or package_info.name('app')

    # Register itself as a language package
    register_package(__name__)

    # Languages set
    define(reg.get('languages', ['en']))

    # Common globals
    register_global('app_name', get_app_name)
    register_global('app@app_name', get_app_name)


_init()

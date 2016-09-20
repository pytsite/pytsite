"""Taxonomy Package Init
"""
# Public API
from . import _api, _model as model, _widget as widget
from ._api import register_model, is_model_registered, find, dispense, build_alias_str, find_by_title, \
    find_by_alias

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, tpl, lang, router, admin, permissions

    # Permissions
    permissions.define_group('taxonomy', 'pytsite.taxonomy@taxonomy')

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # Search term route
    router.add_rule('/taxonomy/search/<model>/<query>', 'pytsite.taxonomy@search_terms')

    # Admin sidebar menu
    admin.sidebar.add_section('taxonomy', __name__ + '@taxonomy', 500, ('*',))


__init()

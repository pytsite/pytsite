"""Taxonomy Package Init
"""
# Public API
from . import _functions, _model as model, _widget as widget
from ._functions import register_model, is_model_registered, find, dispense

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite import assetman, tpl, lang, router, admin

    lang.register_package(__name__)

    tpl.register_package(__name__)
    tpl.register_global('taxonomy', sys.modules[__package__])

    assetman.register_package(__name__)
    assetman.add('pytsite.taxonomy@css/common.css')

    router.add_rule('/pytsite/taxonomy/search/<string:model>/<string:query>', 'pytsite.taxonomy.eps.search_terms')
    admin.sidebar.add_section('taxonomy', __name__ + '@taxonomy', 500, ('*',))

__init()

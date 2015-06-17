"""Taxonomy Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite.core import router, lang
    from pytsite import admin

    lang.register_package(__name__)

    router.add_rule('/pytsite/taxonomy/search/<string:model>/<string:query>',
                    'pytsite.taxonomy.eps.search_terms')

    admin.sidebar.add_section('taxonomy', __name__ + '@taxonomy', 500, ('*',))


__init()

# Public API
from . import _manager, _model, _widget
manager = _manager
model = _model
widget = _widget

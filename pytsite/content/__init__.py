"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite import admin, taxonomy
    from pytsite.core import router, assetman, lang, tpl
    from ._model import Tag, Section

    lang.register_package(__name__)
    tpl.register_global('content', sys.modules[__name__])

    assetman.register_package(__name__)
    assetman.add(__name__ + '@css/common.css', '*')

    # Common routes
    router.add_rule('/content/index/<string:model>', 'pytsite.content.eps.index')
    router.add_rule('/content/view/<string:model>/<string:id>', 'pytsite.content.eps.view')
    router.add_rule('/content/count/<string:model>/<string:id>', 'pytsite.content.eps.view_count')
    router.add_rule('/content/search/<string:model>', 'pytsite.content.eps.search')

    # Propose route
    router.add_rule('/content/propose/<string:model>', 'pytsite.content.eps.propose',
                    filters='pytsite.auth.eps.filter_authorize')
    router.add_rule('/content/propose/<string:model>/submit', 'pytsite.content.eps.propose_submit',
                    filters='pytsite.auth.eps.filter_authorize')

    # Taxonomy models
    taxonomy.register_model('section', Section, __name__ + '@sections')
    taxonomy.register_model('tag', _model.Tag, __name__ + '@tags')

    # Admin elements
    admin.sidebar.add_section('content', __name__ + '@content', 100, ('*',))

__init()


# Public API
from . import _model as model, _widget as widget
from ._functions import register_model, get_models, find, get_model, create

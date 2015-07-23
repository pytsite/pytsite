"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite import admin, taxonomy, settings
    from pytsite.core import router, assetman, lang, tpl, events, odm
    from ._model import Tag, Section, ContentSubscriber
    from ._event_handlers import cron_weekly, router_dispatch
    from ._forms import Settings

    lang.register_package(__name__)
    tpl.register_package(__name__)
    tpl.register_global('content', sys.modules[__name__])

    assetman.register_package(__name__)
    assetman.add(__name__ + '@css/common.css')

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

    # Content subscription routes
    router.add_rule('/content/subscribe', 'pytsite.content.eps.subscribe', methods='POST')
    router.add_rule('/content/unsubscribe/<string:id>', 'pytsite.content.eps.unsubscribe')

    # Taxonomy models
    taxonomy.register_model('section', Section, __name__ + '@sections')
    taxonomy.register_model('tag', _model.Tag, __name__ + '@tags')

    # ODM models
    odm.register_model('content_subscriber', ContentSubscriber)

    # Admin elements
    admin.sidebar.add_section('content', __name__ + '@content', 100, ('*',))

    # Event handlers
    events.listen('pytsite.core.router.dispatch', router_dispatch)
    events.listen('pytsite.core.cron.weekly', cron_weekly)

    # Settings
    settings.define('content', Settings, __name__ + '@content', 'fa fa-file-o',
                    perm_name='pytsite.content.settings',
                    perm_description='content@manage_content_settings_permission')

__init()


# Public API
from . import _model as model, _widget as widget
from ._functions import register_model, get_models, find, get_model, get_model_title, create

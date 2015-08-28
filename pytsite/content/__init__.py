"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite import admin, taxonomy, settings
    from pytsite import console
    from pytsite import assetman
    from pytsite import odm
    from pytsite import events
    from pytsite import tpl
    from pytsite import lang
    from pytsite import router
    from . import _ehs
    from ._model import Tag, Section, ContentSubscriber
    from ._forms import Settings
    from ._console import Generate as GenerateConsoleCommand

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
    events.listen('pytsite.router.dispatch', _ehs.router_dispatch)
    events.listen('pytsite.cron.hourly', _ehs.cron_hourly)
    events.listen('pytsite.cron.daily', _ehs.cron_daily)
    events.listen('pytsite.cron.weekly', _ehs.cron_weekly)
    events.listen('pytsite.update', _ehs.update)

    # Settings
    settings.define('content', Settings, __name__ + '@content', 'fa fa-file-o',
                    perm_name='pytsite.content.settings',
                    perm_description='content@manage_content_settings_permission')

    # Console commands
    console.register_command(GenerateConsoleCommand())


__init()


# Public API
from . import _model as model, _widget as widget
from ._functions import register_model, get_models, find, get_model, get_model_title, create, get_sections

"""Pytsite Content Module.
"""
# Public API
from . import _model as model, _widget as widget
from ._functions import register_model, get_models, find, get_model, get_model_title, create, get_sections, \
    create_section, create_tag, get_tags, get_tag, get_publish_statuses, get_section, is_model_registered

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Module Init Wrapper.
    """
    import sys
    from pytsite import admin, taxonomy, settings, console, assetman, odm, events, tpl, lang, router, robots, browser
    from . import _eh
    from ._model import Tag, Section, ContentSubscriber
    from ._form import Settings
    from ._console_commands import Generate as GenerateConsoleCommand

    lang.register_package(__name__)
    tpl.register_package(__name__)
    tpl.register_global('content', sys.modules[__name__])

    # Assets
    assetman.register_package(__name__)
    browser.include('responsive', True)

    # Common routes
    router.add_rule('/content/index/<string:model>', 'pytsite.content.ep.index')
    router.add_rule('/content/view/<string:model>/<string:id>', 'pytsite.content.ep.view')
    router.add_rule('/content/count/<string:model>/<string:id>', 'pytsite.content.ep.view_count')
    router.add_rule('/content/search/<string:model>', 'pytsite.content.ep.search', call='pytsite.content.ep.index')

    # Propose route
    router.add_rule('/content/propose/<string:model>', 'pytsite.content.ep.propose',
                    filters='pytsite.auth.ep.filter_authorize')
    router.add_rule('/content/propose/<string:model>/submit', 'pytsite.content.ep.propose_submit',
                    filters='pytsite.auth.ep.filter_authorize')

    # Content subscription routes
    router.add_rule('/content/subscribe', 'pytsite.content.ep.subscribe', methods='POST')
    router.add_rule('/content/unsubscribe/<string:id>', 'pytsite.content.ep.unsubscribe')

    # Taxonomy models
    taxonomy.register_model('section', Section, __name__ + '@sections')
    taxonomy.register_model('tag', _model.Tag, __name__ + '@tags')

    # ODM models
    odm.register_model('content_subscriber', ContentSubscriber)

    # Admin elements
    admin.sidebar.add_section('content', __name__ + '@content', 100, ('*',))

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.cron.hourly', _eh.cron_hourly)
    events.listen('pytsite.cron.daily', _eh.cron_daily)
    events.listen('pytsite.cron.weekly', _eh.cron_weekly)
    events.listen('pytsite.update', _eh.update)

    # Settings
    settings.define('content', Settings, __name__ + '@content', 'fa fa-file-o',
                    perm_name='pytsite.content.settings',
                    perm_description=__name__ + '@manage_content_settings_permission')

    # Console commands
    console.register_command(GenerateConsoleCommand())

    # Sitemap location in robots.txt
    robots.sitemap('/sitemap/index.xml')

__init()

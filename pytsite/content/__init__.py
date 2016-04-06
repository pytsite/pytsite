"""Pytsite Content Module.
"""
# Public API
from . import _model as model, _widget as widget
from ._api import register_model, get_models, find, get_model, get_model_title, dispense, get_sections, \
    dispense_section, get_tags, dispense_tag, get_statuses, is_model_registered, generate_rss, find_section_by_title, \
    find_section_by_alias, find_tag_by_alias, find_tag_by_title

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Module Init Wrapper.
    """
    from pytsite import admin, taxonomy, settings, console, assetman, odm, events, tpl, lang, router, robots, browser, \
        ajax
    from . import _eh, _settings
    from ._model import Tag, Section, ContentSubscriber
    from ._console_command import Generate as GenerateConsoleCommand

    lang.register_package(__name__)
    tpl.register_package(__name__)

    # Assets
    assetman.register_package(__name__)
    browser.include('responsive', True)

    # Browser API endpoints
    ajax.register_ep('pytsite.content.ep.view_count')

    # Common routes
    router.add_rule('/content/index/<string:model>', 'pytsite.content.ep.index')
    router.add_rule('/content/view/<string:model>/<string:id>', 'pytsite.content.ep.view')
    router.add_rule('/content/count/<string:model>/<string:id>', 'pytsite.content.ep.view_count')
    router.add_rule('/content/search/<string:model>', 'pytsite.content.ep.search', call='pytsite.content.ep.index')
    router.add_rule('/content/ajax_search/<string:model>', 'pytsite.content.ep.ajax_search')

    # Propose route
    router.add_rule('/content/propose/<string:model>', 'pytsite.content.ep.propose',
                    filters='pytsite.auth.ep.filter_authorize')
    router.add_rule('/content/propose/<string:model>/submit', 'pytsite.content.ep.propose_submit',
                    filters='pytsite.auth.ep.filter_authorize')

    # Content subscription routes
    ajax.register_ep('pytsite.content.ep.subscribe')
    router.add_rule('/content/subscribe', 'pytsite.content.ep.subscribe', methods='POST')
    router.add_rule('/content/unsubscribe/<string:id>', 'pytsite.content.ep.unsubscribe')

    # Taxonomy models
    taxonomy.register_model('section', Section, __name__ + '@sections')
    taxonomy.register_model('tag', Tag, __name__ + '@tags')

    # ODM models
    odm.register_model('content_subscriber', ContentSubscriber)

    # Admin elements
    admin.sidebar.add_section('content', __name__ + '@content', 100, ('*',))

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.cron.hourly', _eh.cron_hourly)
    events.listen('pytsite.cron.daily', _eh.cron_daily)
    events.listen('pytsite.cron.weekly', _eh.cron_weekly)

    # Settings
    settings.define('content', _settings.form_widgets_setup, __name__ + '@content', 'fa fa-file-o',
                    perm_name='pytsite.content.settings',
                    perm_description=__name__ + '@manage_content_settings_permission')

    # Console commands
    console.register_command(GenerateConsoleCommand())

    # Sitemap location in robots.txt
    robots.sitemap('/sitemap/index.xml')


__init()

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
        js_api
    from . import _eh, _settings
    from ._model import Tag, Section, ContentSubscriber
    from ._console_command import Generate as GenerateConsoleCommand

    lang.register_package(__name__)
    tpl.register_package(__name__)

    # Assets
    assetman.register_package(__name__)
    browser.include('responsive', True)

    # Common routes
    router.add_rule('/content/index/<model>', 'pytsite.content@index')
    router.add_rule('/content/view/<model>/<id>', 'pytsite.content@view')
    router.add_rule('/content/count/<model>/<id>', 'pytsite.content@view_count')
    router.add_rule('/content/search/<model>', 'pytsite.content@search', call='pytsite.content@index')
    router.add_rule('/content/ajax_search/<model>', 'pytsite.content@ajax_search')

    # Propose route
    router.add_rule('/content/propose/<model>', 'pytsite.content@propose',
                    filters='pytsite.auth@filter_authorize')
    router.add_rule('/content/propose/<model>/submit', 'pytsite.content@propose_submit',
                    filters='pytsite.auth@filter_authorize')

    # Content subscription routes
    router.add_rule('/content/subscribe', 'pytsite.content@subscribe', methods='POST')
    router.add_rule('/content/unsubscribe/<id>', 'pytsite.content@unsubscribe')

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

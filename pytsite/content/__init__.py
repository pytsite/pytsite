"""Pytsite Content Module.
"""
# Public API
from . import _model as model, _widget as widget
from ._api import register_model, get_models, find, get_model, get_model_title, dispense, get_sections, \
    dispense_section, get_tags, dispense_tag, get_statuses, is_model_registered, generate_rss, find_section_by_title, \
    find_section_by_alias, find_tag_by_alias, find_tag_by_title, find_by_url, paginate

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Module Init Wrapper.
    """
    from pytsite import admin, taxonomy, settings, console, assetman, events, tpl, lang, router, robots, browser, \
        http_api, permissions
    from . import _eh, _settings_form
    from ._model import Tag, Section
    from ._console_command import Generate as GenerateConsoleCommand

    lang.register_package(__name__)
    tpl.register_package(__name__)
    http_api.register_handler('content', 'pytsite.content.http_api')

    # Permission groups
    permissions.define_group('content', 'pytsite.content@content')
    permissions.define_permission('content.settings.manage', __name__ + '@manage_content_settings_permission', 'content')

    # Assets
    assetman.register_package(__name__)
    browser.include('responsive', True)

    # Common routes
    router.add_rule('/content/index/<model>', 'pytsite.content@index')
    router.add_rule('/content/view/<model>/<id>', 'pytsite.content@view')
    router.add_rule('/content/modify/<model>/<id>', 'pytsite.content@modify')
    router.add_rule('/content/search/<model>', 'pytsite.content@search', call='pytsite.content@index')
    router.add_rule('/content/ajax_search/<model>', 'pytsite.content@ajax_search')

    # Propose route
    router.add_rule('/content/propose/<model>', 'pytsite.content@propose',
                    filters='pytsite.auth@f_authorize')
    router.add_rule('/content/propose/<model>/submit', 'pytsite.content@propose_submit',
                    filters='pytsite.auth@f_authorize')

    # Taxonomy models
    taxonomy.register_model('section', Section, __name__ + '@sections')
    taxonomy.register_model('tag', Tag, __name__ + '@tags')

    # Admin elements
    admin.sidebar.add_section('content', __name__ + '@content', 100)

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.setup', _eh.setup)
    events.listen('pytsite.cron.hourly', _eh.cron_hourly)
    events.listen('pytsite.cron.daily', _eh.cron_daily)
    events.listen('pytsite.comments.create_comment', _eh.comments_create_comment)
    events.listen('pytsite.auth.user.delete', _eh.auth_user_delete)

    # Settings
    settings.define('content', _settings_form.Form, __name__ + '@content', 'fa fa-glass', 'content.settings.manage')

    # Console commands
    console.register_command(GenerateConsoleCommand())

    # Sitemap location in robots.txt
    robots.sitemap('/sitemap/index.xml')


_init()

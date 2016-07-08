"""Admin Package Init
"""
# Public API
from . import _sidebar as sidebar, _navbar as navbar
from ._api import render, render_form, base_path

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import assetman, tpl, lang, router, robots, events, browser, permission
    from . import _eh

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # Assets
    bp = base_path()
    browser.include('bootstrap', permanent=True, path_prefix=bp)
    browser.include('font-awesome', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@AdminLTE/css/AdminLTE.min.css', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@AdminLTE/css/skins/skin-blue.min.css', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@css/custom.css', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@AdminLTE/js/app.js', permanent=True, path_prefix=bp, async=True, defer=True)

    # Permissions
    permission.define_permission_group('admin', 'pytsite.admin@admin')
    permission.define_permission('pytsite.admin.use', 'pytsite.admin@use_admin_panel', 'admin')

    # Dashboard route
    router.add_rule(bp, __name__ + '@dashboard')

    sidebar.add_section('misc', 'pytsite.admin@miscellaneous', 500)

    # robots.txt rules
    robots.disallow(base_path() + '/')

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


# Initialization
__init()

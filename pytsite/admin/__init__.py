"""Admin Package Init
"""
# Public API
from . import _sidebar as sidebar, _navbar as navbar
from ._api import render, render_form, base_path

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper.
    """
    from pytsite import assetman, tpl, lang, router, robots, events, browser, permissions
    from . import _eh

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # Assets
    bp = base_path()
    browser.include('bootstrap', permanent=True, path_prefix=bp)
    browser.include('font-awesome', permanent=True, path_prefix=bp)
    browser.include('js-cookie', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@AdminLTE/css/AdminLTE.min.css', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@AdminLTE/css/skins/skin-blue.min.css', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@css/custom.css', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@AdminLTE/js/app.js', permanent=True, path_prefix=bp)
    assetman.add('pytsite.admin@js/admin.js', permanent=True, path_prefix=bp)

    # Permissions
    permissions.define_permission('pytsite.admin.use', 'pytsite.admin@use_admin_panel', 'app')

    # Dashboard route
    router.add_rule(bp, __name__ + '@dashboard')

    # Tpl globals
    tpl.register_global('admin_url', base_path)

    sidebar.add_section('misc', 'pytsite.admin@miscellaneous', 500)

    # robots.txt rules
    robots.disallow(bp + '/')

    # Event handlers
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


# Initialization
_init()

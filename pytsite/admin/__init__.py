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
    from pytsite import assetman, tpl, lang, router, robots, permissions
    from . import _eh, _controllers

    bp = base_path()

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # JS modules
    assetman.js_module('pytsite-admin-lte', __name__ + '@AdminLTE/js/app', True, ['jquery', 'twitter-bootstrap'])

    # Assetman tasks
    assetman.t_js(__name__ + '@**')
    assetman.t_css(__name__ + '@**')
    assetman.t_less(__name__ + '@**')

    # Assets
    assetman.preload('font-awesome', True, path_prefix=bp)
    assetman.preload('twitter-bootstrap', True, path_prefix=bp)
    assetman.preload('pytsite.admin@AdminLTE/css/AdminLTE.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@AdminLTE/css/skins/skin-blue.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@css/custom.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@css/admin-form.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@js/pytsite-admin.js', True, path_prefix=bp)

    # Permissions
    permissions.define_permission('pytsite.admin.use', 'pytsite.admin@use_admin_panel', 'app')

    # Dashboard route
    router.handle(_controllers.Dashboard(), bp, 'pytsite.admin@dashboard')

    # Tpl globals
    tpl.register_global('admin_base_path', bp)

    sidebar.add_section('misc', 'pytsite.admin@miscellaneous', 500)

    # robots.txt rules
    robots.disallow(bp + '/')

    # Event handlers
    router.on_dispatch(_eh.router_dispatch)


# Initialization
_init()

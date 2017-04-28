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
    from pytsite import assetman, tpl, lang, router, robots, browser, permissions
    from . import _eh

    bp = base_path()

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # Assetman tasks
    assetman.t_js('pytsite.admin@**/*.js')
    assetman.t_css('pytsite.admin@**/*.css')
    assetman.t_less('pytsite.admin@**/*.less')

    # Assets
    assetman.preload('font-awesome', True, path_prefix=bp)
    assetman.preload('twitter-bootstrap', True)
    assetman.preload('pytsite.admin@AdminLTE/css/AdminLTE.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@AdminLTE/css/skins/skin-blue.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@css/custom.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@css/admin-form.css', True, path_prefix=bp)
    assetman.preload('pytsite.admin@js/index.js', True, path_prefix=bp)

    # Permissions
    permissions.define_permission('pytsite.admin.use', 'pytsite.admin@use_admin_panel', 'app')

    # Dashboard route
    router.handle(bp, 'pytsite.admin@dashboard', 'pytsite.admin@dashboard')

    # Tpl globals
    tpl.register_global('admin_base_path', bp)

    sidebar.add_section('misc', 'pytsite.admin@miscellaneous', 500)

    # robots.txt rules
    robots.disallow(bp + '/')

    # Event handlers
    router.on_dispatch(_eh.router_dispatch)


# Initialization
_init()

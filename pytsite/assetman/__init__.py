"""PytSite Asset Manager.
"""
# Public API
from . import _error as error
from ._api import register_package, library, preload, remove, dump_js, dump_css, url, add_inline, dump_inline, \
    get_urls, get_locations, reset, detect_collection, build, is_package_registered, register_global, _add_task, \
    t_browserify, t_copy, t_copy_static, t_less, t_js, t_css, js_module, setup

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from os import path
    from pytsite import reg, console, events, lang, tpl, router, setup as pytsite_setup
    from . import _console_command, _api

    # Registry variables
    reg.put('paths.assets', path.join(reg.get('paths.static'), 'assets'))

    # Resources
    lang.register_package(__name__)

    # Console commands
    console.register_command(_console_command.Setup())
    console.register_command(_console_command.Build())

    # Event handlers
    router.on_dispatch(reset, -999)
    router.on_xhr_dispatch(reset, -999, 'post')  # Workaround for forms
    pytsite_setup.on_setup(setup)
    events.listen('pytsite.update.after', lambda: build(switch_maintenance=False))

    # Tpl resources
    tpl.register_package(__name__)
    tpl.register_global('asset_url', url)
    tpl.register_global('css_links', dump_css)
    tpl.register_global('js_links', dump_js)
    tpl.register_global('js_head_links', lambda: dump_js(head=True))
    tpl.register_global('inline_js', dump_inline)

    # Register assetman itself and add required assets for all pages
    register_package(__name__)
    js_module('assetman', __name__ + '@assetman')
    t_js(__name__ + '@**')
    preload(__name__ + '@require.js', permanent=True, head=True)
    preload(__name__ + '@require-config.js', permanent=True, head=True)


_init()

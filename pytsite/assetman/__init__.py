"""PytSite Asset Manager.
"""
# Public API
from os import path as _path
from pytsite import reg as _reg
from . import _error as error
from ._api import register_package, library, preload, remove, dump_js, dump_css, url, add_inline, dump_inline, \
    get_urls, get_locations, reset, detect_collection, build, build_all, is_package_registered, register_global, \
    t_browserify, t_copy, t_copy_static, t_less, t_js, t_css, js_module, setup, get_src_dir_path, get_dst_dir_path

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# It is important to call this before any other imports from pytsite
_reg.put('paths.assets', _path.join(_reg.get('paths.static'), 'assets'))


def _init():
    from pytsite import console, lang, tpl, router, setup as pytsite_setup, update as pytsite_update
    from . import _console_commands, _api

    # Resources
    lang.register_package(__name__)

    # Do this here to avoid cyclic dependency
    register_package('pytsite.lang')
    t_js('pytsite.lang@**')
    js_module('pytsite-lang-translations', 'pytsite.lang@translations')
    js_module('pytsite-lang', 'pytsite.lang@pytsite-lang')

    # Console commands
    console.register_command(_console_commands.Setup())
    console.register_command(_console_commands.Build())

    # Event handlers
    router.on_dispatch(reset, -999, '*')
    router.on_xhr_dispatch(reset, -999, '*')
    pytsite_setup.on_setup(setup)
    pytsite_update.on_update_after(build_all)
    pytsite_update.on_update_after(lang.build)

    # Tpl resources
    tpl.register_package(__name__)
    tpl.register_global('asset_url', url)
    tpl.register_global('css_links', dump_css)
    tpl.register_global('js_links', dump_js)
    tpl.register_global('js_head_links', lambda: dump_js(head=True))
    tpl.register_global('inline_js', dump_inline)

    # Register assetman itself and add required assets for all pages
    register_package(__name__)

    js_module('assetman-build-timestamps', __name__ + '@build-timestamps')
    js_module('assetman', __name__ + '@assetman')

    t_js(__name__ + '@**')

    preload(__name__ + '@require.js', permanent=True, head=True)
    preload(__name__ + '@require-config.js', permanent=True, head=True)


_init()

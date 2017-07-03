"""PytSite Auth Profile
"""
from . import _widget as widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, tpl, router, auth_web, assetman
    from . import _controllers

    lang.register_package(__name__)
    tpl.register_package(__name__)

    bp = auth_web.base_path()
    router.handle(_controllers.ProfileView(), bp + '/profile/<nickname>', 'pytsite.auth_profile@profile_view')
    router.handle(_controllers.ProfileEdit(), bp + '/profile/<nickname>/edit', 'pytsite.auth_profile@profile_edit',
                  filters='pytsite.auth_web@authorize')

    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.t_less(__name__ + '@**')
    assetman.js_module('pytsite-auth-widget-follow', __name__ + '@js/pytsite-auth-widget-follow')
    assetman.js_module('pytsite-auth-widget-profile', __name__ + '@js/pytsite-auth-widget-profile')


_init()

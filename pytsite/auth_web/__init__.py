"""PytSite Auth HTTP Parts
"""
from ._api import base_path, sign_in_form, user_modify_form, sign_in_url, sign_out_url

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import auth, router, robots, assetman, lang, tpl
    from . import _controllers, _eh

    # Localization resources
    lang.register_package(__name__)

    # Routes
    bp = base_path()
    router.handle(_controllers.FilterAuthorize(), name='pytsite.auth_web@authorize')
    router.handle(_controllers.SignIn(), bp + '/sign-in/<driver>', 'pytsite.auth_web@sign_in')
    router.handle(_controllers.SignInSubmit(), bp + '/sign-in/<driver>/post', 'pytsite.auth_web@sign_in_submit',
                  methods='POST')
    router.handle(_controllers.SignOut(), bp + '/sign-out', 'pytsite.auth_web@sign_out')

    # Router events
    router.on_dispatch(_eh.router_dispatch, -999, '*')
    router.on_xhr_dispatch(_eh.router_dispatch, -999, '*')
    router.on_response(_eh.router_response, -999, '*')
    router.on_xhr_response(_eh.router_response, -999, '*')

    # Template engine globals
    tpl.register_package(__name__)
    tpl.register_global('auth_current_user', auth.get_current_user)
    tpl.register_global('auth_sign_in_url', sign_in_url)
    tpl.register_global('auth_sign_out_url', sign_out_url)

    # Assets
    assetman.register_package(__name__)
    assetman.t_less(__name__ + '@**')

    # robots.txt rules
    robots.disallow(bp + '/')


_init()

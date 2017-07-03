""" PytSite Auth HTTP API
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import http_api, assetman
    from . import _controllers, _eh

    # Access token HTTP API
    http_api.handle('POST', 'auth/access-token/<driver>', _controllers.PostAccessToken(),
                    'pytsite.auth@post_access_token')
    http_api.handle('GET', 'auth/access-token/<token>', _controllers.GetAccessToken(),
                    'pytsite.auth@get_access_token')
    http_api.handle('DELETE', 'auth/access-token/<token>', _controllers.DeleteAccessToken(),
                    'pytsite.auth@delete_access_token')

    # User HTTP API
    http_api.handle('GET', 'auth/is_anonymous', _controllers.IsAnonymous(), 'pytsite.auth@is_anonymous')
    http_api.handle('GET', 'auth/user/<uid>', _controllers.GetUser(), 'pytsite.auth@get_user')
    http_api.handle('PATCH', 'auth/user/<uid>', _controllers.PatchUser(), 'pytsite.auth@patch_user')

    # Following HTTP API
    http_api.handle('POST', 'auth/follow/<uid>', _controllers.PostFollow(), 'pytsite.auth@post_follow')
    http_api.handle('DELETE', 'auth/follow/<uid>', _controllers.DeleteFollow(), 'pytsite.auth@delete_follow')

    http_api.on_pre_request(_eh.http_api_pre_request)

    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.js_module('pytsite-auth-http-api', __name__ + '@js/pytsite-auth-http-api')


_init()

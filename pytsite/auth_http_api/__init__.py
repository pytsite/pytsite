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
    http_api.handle('GET', 'auth/users', _controllers.GetUsers(), 'pytsite.auth@get_users')
    http_api.handle('PATCH', 'auth/user/<uid>', _controllers.PatchUser(), 'pytsite.auth@patch_user')

    # Following HTTP API
    http_api.handle('GET', 'auth/follows/<uid>', _controllers.GetFollowsOrFollowers(), 'pytsite.auth@get_follows')
    http_api.handle('GET', 'auth/followers/<uid>', _controllers.GetFollowsOrFollowers(), 'pytsite.auth@get_followers')
    http_api.handle('POST', 'auth/follow/<uid>', _controllers.PostFollow(), 'pytsite.auth@post_follow')
    http_api.handle('DELETE', 'auth/follow/<uid>', _controllers.DeleteFollow(), 'pytsite.auth@delete_follow')

    # Block users HTTP API
    http_api.handle('POST', 'auth/block_user/<uid>', _controllers.PostBlockUser(), 'pytsite.auth@post_block_user')
    http_api.handle('DELETE', 'auth/block_user/<uid>', _controllers.DeleteBlockUser(), 'pytsite.auth@delete_block_user')
    http_api.handle('GET', 'auth/blocked_users/<uid>', _controllers.GetBlockedUsers(), 'pytsite.auth@get_blocked_users')

    http_api.on_pre_request(_eh.http_api_pre_request)

    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.js_module('pytsite-auth-http-api', __name__ + '@js/pytsite-auth-http-api')


_init()

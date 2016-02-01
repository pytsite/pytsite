"""Facebook Sessions.
"""
from collections import Generator as _Generator
import requests as _requests
from pytsite import router as _router, util as _util, reg as _reg
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_API_REQUEST_URL = 'https://graph.facebook.com/v2.5/'
_states = {}


class AuthSession:
    """Facebook Authorization Session.
    """
    def __init__(self, state: str=None, redirect_uri: str=None):
        """Init.
        """
        self._app_id = _reg.get('fb.app_id')
        self._app_secret = _reg.get('fb.app_secret')

        if state:
            self._state = state
            self._final_redirect_uri = _states.get(state, _router.current_url())
        else:
            self._state = _util.random_str(64)
            self._final_redirect_uri = redirect_uri if redirect_uri else _router.current_url()
            _states[self._state] = self._final_redirect_uri

    @property
    def redirect_uri(self) -> str:
        return self._final_redirect_uri

    def get_authorization_url(self, scope='public_profile,email,user_friends') -> str:
        """Get authorization URL which used to point user for authorization.
        """
        return _router.url('https://www.facebook.com/dialog/oauth', query={
            'client_id': self._app_id,
            'state': self._state,
            'redirect_uri': _router.ep_url('pytsite.fb.ep.authorize'),
            'scope': scope,
        })

    def get_access_token(self, auth_code: str) -> dict:
        """Get access token from Facebook.
        """
        url = _router.url(_API_REQUEST_URL + 'oauth/access_token', query={
            'client_id': self._app_id,
            'client_secret': self._app_secret,
            'redirect_uri': _router.ep_url('pytsite.fb.ep.authorize'),
            'code': auth_code,
        })

        r = _requests.get(url).json()
        if 'error' in r:
            raise _error.AuthSessionError(r['error']['message'])

        return r


class Session:
    """Facebook Session.
    """
    def __init__(self, access_token: str):
        """Init.
        """
        self._app_id = _reg.get('fb.app_id')
        self._app_secret = _reg.get('fb.app_secret')
        self._access_token = access_token

        if not self._access_token:
            raise _error.SessionError('access_token is empty.')

    def request(self, endpoint, method='GET', **kwargs) -> dict:
        """Perform request.
        """
        if method.upper() == 'POST':
            params = {'access_token': self._access_token}
            return _requests.post(_API_REQUEST_URL + endpoint, params=params, data=kwargs).json()
        else:
            kwargs['access_token'] = self._access_token
            return _requests.get(_API_REQUEST_URL + endpoint, params=kwargs).json()

    def paginated_request(self, endpoint, **kwargs) -> _Generator:
        """Perform paginated request.
        """
        r = self.request(endpoint, **kwargs)
        if 'data' not in r:
            raise Exception("Endpoint '{}' didn't return paginated response. Details: {}".format(endpoint, r))

        while True:
            for item in r['data']:
                yield item
            if 'next' in r:
                r = self.request(endpoint)
            else:
                break

    def me(self) -> dict:
        """Get information about authenticated user.
        """
        return self.request('me')

    def accounts(self, user_id: int=None) -> _Generator:
        """Get user's accounts.
        """
        if not user_id:
            user_id = 'me'

        return self.paginated_request('{}/accounts'.format(user_id))

    def feed_message(self, message: str=None, link: str=None, user_id: int=None, link_picture: str=None,
                     link_title: str=None, link_caption: str=None, link_description: str=None):
        """Post a message on user's feed.
        """
        # https://developers.facebook.com/docs/graph-api/reference/v2.5/user/feed/#publish
        if not message and not link:
            raise ValueError('Either message or link is required.')

        if not user_id:
            user_id = 'me'

        return self.request('{}/feed'.format(user_id), 'POST', message=message, link=link, picture=link_picture,
                            name=link_title, caption=link_caption, description=link_description)

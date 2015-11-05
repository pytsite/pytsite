"""Facebook Sessions.
"""
from collections import Generator as _Generator
import requests as _requests
from pytsite import router as _router, util as _util, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_API_REQUEST_URL = 'https://graph.facebook.com/v2.5/'
_states = {}


class AuthSession():
    def __init__(self, state: str=None, final_redirect_uri: str=None):
        self._app_id = _reg.get('fb.app_id')
        self._app_secret = _reg.get('fb.app_secret')

        if state:
            self._state = state
            self._final_redirect_uri = _states.get(state, _router.current_url())
        else:
            self._state = _util.random_str(64)
            self._final_redirect_uri = final_redirect_uri if final_redirect_uri else _router.current_url()
            _states[self._state] = self._final_redirect_uri

    @property
    def final_redirect_uri(self) -> str:
        return self._final_redirect_uri

    def get_authorization_url(self, scope='public_profile,email,user_friends') -> str:
        return _router.url('https://www.facebook.com/dialog/oauth', query={
            'client_id': self._app_id,
            'state': self._state,
            'redirect_uri': _router.ep_url('pytsite.fb.ep.authorize'),
            'scope': scope,
        })

    def get_access_token(self, auth_code: str) -> dict:
        url = _router.url(_API_REQUEST_URL + 'oauth/access_token', query={
            'client_id': self._app_id,
            'client_secret': self._app_secret,
            'redirect_uri': _router.ep_url('pytsite.fb.ep.authorize'),
            'code': auth_code,
        })

        return _requests.get(url).json()


class Session():
    def __init__(self, access_token: str):
        self._app_id = _reg.get('fb.app_id')
        self._app_secret = _reg.get('fb.app_secret')
        self._access_token = access_token

    def request(self, endpoint, method='GET', **kwargs) -> dict:
        if method.upper() == 'POST':
            params = {'access_token': self._access_token}
            return _requests.post(_API_REQUEST_URL + endpoint, params=params, data=kwargs).json()
        else:
            kwargs['access_token'] = self._access_token
            return _requests.get(_API_REQUEST_URL + endpoint, params=kwargs).json()

    def paginated_request(self, endpoint, **kwargs) -> _Generator:
        r = self.request(endpoint, 'GET', **kwargs)
        if 'paging' not in r:
            raise Exception("Endpoint '{}' didn't return paginated response.")

        while True:
            for item in r['data']:
                yield item
            if 'next' in r:
                r = self.request(endpoint, 'GET', )
            else:
                break

    def me(self) -> dict:
        return self.request('me')

    def accounts(self, user_id: int=None) -> _Generator:
        if not user_id:
            user_id = 'me'

        return self.paginated_request('{}/accounts'.format(user_id))

    def feed_message(self, msg: str, user_id: int=None) -> dict:
        # https://developers.facebook.com/docs/graph-api/reference/v2.5/user/feed/#publish
        if not user_id:
            user_id = 'me'

        return self.request('{}/feed'.format(user_id), 'POST', message=msg)

    def feed_link(self, link: str, user_id: int=None, picture: str=None, name: str=None, caption: str=None,
                  description: str=None):
        # https://developers.facebook.com/docs/graph-api/reference/v2.5/user/feed/#publish
        if not user_id:
            user_id = 'me'

        return self.request('{}/feed'.format(user_id), 'POST', link=link, picture=picture, name=name, caption=caption,
                            description=description)

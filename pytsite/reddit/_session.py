"""Reddit Session.
"""
import requests as _requests
from pytsite import reg as _reg, router as _router, validation as _validation, util as _util, version as _pytsite_ver
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_USER_AGENT = 'python:pytsite:{} (by /u/aleshep)'.format(_pytsite_ver())
_API_BASE_URL = 'https://www.reddit.com/api/v1/'
_API_REQUEST_URL = 'https://oauth.reddit.com/'
_states = {}


class AuthSession():
    def __init__(self, state: str=None, redirect_uri: str=None):
        self._app_key = _reg.get('reddit.app_key')
        self._app_secret = _reg.get('reddit.app_secret')

        if state:
            self._state = state
            self._redirect_uri = _states.get(state, _router.current_url())
        else:
            self._state = _util.random_str(64)
            self._redirect_uri = redirect_uri if redirect_uri else _router.current_url()
            _states[self._state] = self._redirect_uri

    @property
    def redirect_uri(self) -> str:
        return self._redirect_uri

    def get_authorization_url(self) -> str:
        return _router.url(_API_BASE_URL + 'authorize', query={
            'client_id': self._app_key,
            'response_type': 'code',
            'state': self._state,
            'redirect_uri': _router.ep_url('pytsite.reddit.ep.authorize'),
            'duration': 'permanent',
            'scope': 'identity,edit,flair,history,modconfig,modflair,modlog,modposts,modwiki,mysubreddits,'
                     'privatemessages,read,report,save,submit,subscribe,vote,wikiedit,wikiread',
        })

    def get_access_token(self, auth_code: str) -> dict:
        r = _requests.post(_API_BASE_URL + 'access_token', data={
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': _router.ep_url('pytsite.reddit.ep.authorize'),
        }, headers={
            'User-Agent': _USER_AGENT,
        }, auth=(self._app_key, self._app_secret))

        return r.json()


class Session():
    def __init__(self, access_token: str):
        self._app_key = _reg.get('reddit.app_key')
        self._app_secret = _reg.get('reddit.app_secret')
        self._access_token = access_token

    def request(self, endpoint: str, method='GET', **kwargs):
        if method.upper() == 'POST':
            r = _requests.post(_API_REQUEST_URL + endpoint, data=kwargs, headers={
                'User-Agent': _USER_AGENT,
                'Authorization': 'bearer ' + self._access_token,
            })
        else:
            r = _requests.get(_API_REQUEST_URL + endpoint, data=kwargs, headers={
                'User-Agent': _USER_AGENT,
                'Authorization': 'bearer ' + self._access_token,
            })

        if r.status_code < 200 or r.status_code > 299:
            if r.status_code == 401:
                raise _error.Unauthorized()
            else:
                raise _error.RequestError(r.text)

        return r.json()

    def refresh_access_token(self, refresh_token) -> dict:
        r = _requests.post(_API_BASE_URL + 'access_token', data={
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }, headers={
            'User-Agent': _USER_AGENT,
        }, auth=(self._app_key, self._app_secret))

        return r.json()

    def user_info(self) -> dict:
        return self.request('api/v1/me')

    def subreddits_mine(self, where: str):
        return self.request('subreddits/mine/{}'.format(where))

    def submit_link(self, subreddit: str, url: str):
        return self.request('api/submit', 'POST', sr=subreddit, url=url)

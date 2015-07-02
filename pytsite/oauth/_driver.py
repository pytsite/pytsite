"""oAuth Base Session.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod
from requests_oauthlib import OAuth1Session
from datetime import datetime as _dt
from pytsite.core import reg as _reg, router as _router


class Driver(_ABC):
    """Abstract oAuth session.
    """
    @_abstractmethod
    def get_authorization_url(self) -> str:
        pass


class Twitter(Driver):
    def __init__(self, oauth_token: str=None, oauth_token_secret: str=None):
        """Init.
        """
        self._client_key = _reg.get('oauth.twitter.key')
        self._client_secret = _reg.get('oauth.twitter.secret')

        if not oauth_token and not oauth_token_secret:
            state = self._get_state()
            # Need to fetch request token
            if state['stage'] == 'new':
                oauth = OAuth1Session(self._client_key, self._client_secret,
                                      callback_uri=_router.current_url(True))
                r_token_resp = oauth.fetch_request_token('https://api.twitter.com/oauth/request_token')
                self._set_state({
                    'stage': 'request_token',
                    'time': _dt.now(),
                    'oauth_token': r_token_resp.get('oauth_token'),
                    'oauth_token_secret': r_token_resp.get('oauth_token_secret')
                })

    def _get_state(self) -> dict:
        default = {
            'stage': 'new',
            'time': _dt.now(),
            'oauth_token': None,
            'oauth_token_secret': None
        }
        state = _router.session.get('oauth.twitter.session')

        if not state or (_dt.now() - state['time']).seconds > 60:
            state = default

        return state

    def _set_state(self, state: dict):
        _router.session['oauth.twitter.session'] = state
        return self

    def _clear_state(self):
        if 'oauth.twitter.session' in _router.session:
            del _router.session['oauth.twitter.session']
        return self

    def get_authorization_url(self) -> str:
        state = self._get_state()
        if state['stage'] != 'request_token':
            raise Exception("Cannot generate authorization URL.")

        oauth = OAuth1Session(self._client_key, self._client_secret,
                              state['oauth_token'], state['oauth_token_secret'],
                              callback_uri=_router.current_url(True))

        return oauth.authorization_url('https://api.twitter.com/oauth/authorize')

    def get_access_token(self, verifier: str) -> dict:
        state = self._get_state()
        if state['stage'] != 'request_token':
            raise Exception('Session expired')

        session = OAuth1Session(self._client_key, self._client_secret,
                                state['oauth_token'], state['oauth_token_secret'],
                                _router.current_url(True), verifier=verifier)

        token = session.fetch_access_token('https://api.twitter.com/oauth/access_token')
        self._clear_state()
        return token

"""Twitter oAuth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from requests_oauthlib import OAuth1Session
from datetime import datetime as _dt
from pytsite.core import reg as _reg, router as _router, widget as _widget, html as _html, lang as _lang
from pytsite import oauth as _oauth


class Widget(_widget.Base):
    """Twitter oAuth Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._oauth_token = kwargs.get('oauth_token', '')
        self._oauth_token_secret = kwargs.get('oauth_token_secret', '')
        self._user_id = kwargs.get('user_id', '')
        self._screen_name = kwargs.get('screen_name', '')

    def render(self) -> _html.Element:
        """Render widget.
        """
        driver = _oauth.load_driver('twitter', oauth_token=self._oauth_token,
                                    oauth_token_secret=self._oauth_token_secret)
        """:type: pytsite.twitter._oauth.Driver"""

        # If 'verifier' is here, we need to exchange it to an access token
        inp_oauth_verifier = _router.request.values_dict.get('oauth_verifier')
        if inp_oauth_verifier:
            token = driver.get_access_token(inp_oauth_verifier)
            self._oauth_token = token['oauth_token']
            self._oauth_token_secret = token['oauth_token_secret']
            self._user_id = token['user_id']
            self._screen_name = token['screen_name']

        wrapper = _html.Div()
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'oauth_token'),
                                   value=self._oauth_token))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'oauth_token_secret'),
                                   value=self._oauth_token_secret))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'user_id'),
                                   value=self._user_id))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'screen_name'),
                                   value=self._screen_name))

        if self._screen_name:
            title = self._screen_name
            href = 'https://twitter.com/' + self._screen_name
        else:
            title = _lang.t('pytsite.twitter@authorization')
            href = driver.get_authorization_url()

        a = _html.A(title, href=href).append(_html.I(cls='fa fa-twitter'))
        wrapper.append(a)

        return self._group_wrap(wrapper)


class Driver(_oauth.AbstractDriver):
    """Twitter oAuth Driver.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        self._client_key = _reg.get('twitter.app_key')
        self._client_secret = _reg.get('twitter.app_secret')
        self._oauth_token = kwargs.get('oauth_token')
        self._oauth_token_secret = kwargs.get('oauth_token_secret')

    def _init_session(self):
        if self._get_state()['stage'] == 'new':
            # Need to fetch request token
            oauth = OAuth1Session(self._client_key, self._client_secret, callback_uri=_router.current_url())
            r_token_resp = oauth.fetch_request_token('https://api.twitter.com/oauth/request_token')
            self._set_state({
                'stage': 'request_token',
                'time': _dt.now(),
                'oauth_token': r_token_resp.get('oauth_token'),
                'oauth_token_secret': r_token_resp.get('oauth_token_secret')
            })

    def _get_state(self) -> dict:
        """Get state.
        """
        if self._oauth_token and self._oauth_token_secret:
            return {'stage': 'ready'}

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
        """Set state.
        """
        _router.session['oauth.twitter.session'] = state
        return self

    def _clear_state(self):
        """Clear state.
        """
        if 'oauth.twitter.session' in _router.session:
            del _router.session['oauth.twitter.session']
        return self

    def get_authorization_url(self) -> str:
        """Get authorization URL.
        """
        self._init_session()

        state = self._get_state()
        if state['stage'] != 'request_token':
            raise Exception("Cannot generate authorization URL.")

        oauth = OAuth1Session(self._client_key, self._client_secret,
                              state['oauth_token'], state['oauth_token_secret'],
                              callback_uri=_router.current_url())

        return oauth.authorization_url('https://api.twitter.com/oauth/authorize')

    def get_access_token(self, verifier: str) -> dict:
        """Exchange request token to access token.
        """
        self._init_session()

        state = self._get_state()
        if state['stage'] != 'request_token':
            raise Exception('Session expired')
        self._clear_state()

        session = OAuth1Session(self._client_key, self._client_secret,
                                state['oauth_token'], state['oauth_token_secret'],
                                verifier=verifier)

        return session.fetch_access_token('https://api.twitter.com/oauth/access_token')

    def get_widget(self, uid: str, **kwargs) -> _widget.Base:
        """Get widget.
        """
        return Widget(uid=uid, **kwargs)

"""oAuth Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from requests_oauthlib import OAuth1Session
from pytsite.core import widget as _widget, html as _html, lang as _lang, router as _router
from . import _driver


class Twitter(_widget.base.Base):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._oauth_token = kwargs.get('oauth_token', '')
        self._oauth_token_secret = kwargs.get('oauth_token_secret', '')
        self._user_id = kwargs.get('user_id', '')
        self._screen_name = kwargs.get('screen_name', '')

    def _request_token(self):
        pass

    def render(self) -> _html.Element:
        driver = _driver.Twitter()

        inp_oauth_verifier = _router.request.values_dict.get('oauth_verifier')
        if inp_oauth_verifier:
            token = driver.get_access_token(inp_oauth_verifier)
            self._oauth_token = token['oauth_token']
            self._oauth_token_secret = token['oauth_token_secret']
            self._user_id = token['user_id']
            self._screen_name = token['screen_name']

        wrapper = _html.Div()
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self.uid, 'oauth_token'),
                                   value=self._oauth_token))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self.uid, 'oauth_token_secret'),
                                   value=self._oauth_token_secret))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self.uid, 'user_id'),
                                   value=self._user_id))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self.uid, 'screen_name'),
                                   value=self._screen_name))

        if self._screen_name:
            title = self._screen_name
            href = 'https://twitter.com/' + self._screen_name
        else:
            title = _lang.t('pytsite.oauth@sign_in')
            href = driver.get_authorization_url()

        a = _html.A(title, href=href)
        a.append(_html.I(cls='fa fa-twitter'))

        wrapper.append(a)

        return self._group_wrap(wrapper)

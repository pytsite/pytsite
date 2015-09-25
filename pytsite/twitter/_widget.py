"""Twitter oAuth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite import widget as _widget, html as _html, lang as _lang, assetman as _assetman, router as _router
from ._session import Session as TwitterSession


class Auth(_widget.Base):
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

        _assetman.add('pytsite.twitter@widget.js')

        self._css += ' widget-twitter-oauth'

    def render(self) -> _html.Element:
        """Render widget.
        """
        session = TwitterSession(oauth_token=self._oauth_token, oauth_token_secret=self._oauth_token_secret)
        """:type: pytsite.twitter._oauth.Driver"""

        # If 'verifier' is here, we need to exchange it to an access token
        inp_oauth_verifier = _router.request.values_dict.get('oauth_verifier')
        if inp_oauth_verifier:
            token = session.get_access_token(inp_oauth_verifier)
            self._oauth_token = token['oauth_token']
            self._oauth_token_secret = token['oauth_token_secret']
            self._user_id = token['user_id']
            self._screen_name = token['screen_name']

        wrapper = _html.Div()
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._entity, 'oauth_token'),
                                   value=self._oauth_token))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._entity, 'oauth_token_secret'),
                                   value=self._oauth_token_secret))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._entity, 'user_id'),
                                   value=self._user_id))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._entity, 'screen_name'),
                                   value=self._screen_name))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._entity, 'title'),
                                   value=self._screen_name))

        if self._screen_name:
            title = self._screen_name
            href = 'https://twitter.com/' + self._screen_name
        else:
            title = _lang.t('pytsite.twitter@authorization')
            href = session.get_authorization_url()

        a = _html.A(title, href=href).append(_html.I(cls='fa fa-twitter'))
        wrapper.append(a)

        return self._group_wrap(wrapper)

"""Tumblr Auth Widget.
"""
import pytsite.widget._base
from pytsite import widget as _widget, html as _html, lang as _lang, router as _router
from ._session import Session as TumblrSession, AuthSession as TumblrAuthSession

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Auth(_widget.Base):
    """Twitter oAuth Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._oauth_token = kwargs.get('oauth_token', '')
        self._oauth_token_secret = kwargs.get('oauth_token_secret', '')
        self._screen_name = kwargs.get('screen_name', '')
        self._user_blogs = []
        self._user_blog = kwargs.get('user_blog', '')
        self._callback_uri = kwargs.get('callback_uri', _router.current_url())

        self._css += ' widget-tumblr-oauth'

    @property
    def oauth_token(self) -> str:
        return self._oauth_token

    @property
    def oauth_token_secret(self) -> str:
        return self._oauth_token_secret

    @property
    def screen_name(self) -> str:
        return self._screen_name

    @property
    def user_blogs(self) -> str:
        return self._user_blogs

    @property
    def user_blog(self) -> str:
        return self._user_blog

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render widget.
        :param **kwargs:
        """
        # If 'verifier' is here, we need to exchange it to an access token
        inp_oauth_token = _router.request().inp.get('oauth_token')
        inp_oauth_verifier = _router.request().inp.get('oauth_verifier')
        if inp_oauth_token and inp_oauth_verifier:
            access_data = TumblrAuthSession(inp_oauth_token).get_access_token(self._callback_uri)
            self._oauth_token = access_data['oauth_token']
            self._oauth_token_secret = access_data['oauth_token_secret']
            user_info = TumblrSession(self._oauth_token, self._oauth_token_secret).user_info()
            self._screen_name = user_info['name']

        if self._oauth_token and self._oauth_token_secret and self._screen_name:
            user_info = TumblrSession(self._oauth_token, self._oauth_token_secret).user_info()
            self._user_blogs = [(i['name'], i['title']) for i in user_info['blogs']]

        wrapper = _widget.Container(self.uid)

        wrapper.add_widget(_widget.input.Hidden(
            uid=self.uid + '[oauth_token]',
            value=self.oauth_token,
        ))

        wrapper.add_widget(_widget.input.Hidden(
            uid=self.uid + '[oauth_token_secret]',
            value=self.oauth_token_secret,
        ))

        wrapper.add_widget(_widget.input.Hidden(
            uid=self.uid + '[screen_name]',
            value=self.screen_name,
        ))

        if self.user_blogs:
            a = _html.A('&nbsp;{}'.format(self.screen_name), href='http://{}.tumblr.com'.format(self.screen_name),
                        target='_blank')
            a.append(_html.I(cls='fa fa-fw fa-tumblr'))

            wrapper.add_widget(_widget.static.HTML(self.uid + '[user]', em=a))
            wrapper.add_widget(_widget.select.Select(
                uid=self.uid + '[user_blog]',
                h_size='col-sm-6',
                items=self.user_blogs,
                value=self.user_blog,
                required=True,
                label=_lang.t('pytsite.tumblr@blog')
            ))
        else:
            auth_s = TumblrAuthSession(callback_uri=self._callback_uri).fetch_request_token()
            a = _html.A(_lang.t('pytsite.tumblr@authorization'), href=auth_s.get_authorization_url())
            a.append(_html.I(cls='fa fa-fw fa-tumblr'))
            wrapper.add_widget(_widget.static.HTML(self.uid + '[user]', em=a))

        return self._group_wrap(wrapper)

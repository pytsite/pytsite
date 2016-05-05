"""Facebook Widgets.
"""
from datetime import datetime as _datetime
from pytsite import widget as _widget, html as _html, reg as _reg, router as _router, assetman as _assetman, \
    lang as _lang, tpl as _tpl
from ._session import AuthSession as _AuthSession, Session as _Session

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Auth(_widget.Base):
    """Facebook Authorization Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._app_id = _reg.get('fb.app_id')
        self._app_secret = _reg.get('fb.app_secret')
        self._scope = kwargs.get('scope', 'public_profile,email,user_friends')
        self._access_token = kwargs.get('access_token', '')
        self._access_token_type = kwargs.get('access_token_type', '')
        self._access_token_expires = kwargs.get('access_token_expires', 0)
        self._user_id = kwargs.get('user_id', '')
        self._pages = []
        self._page_id = kwargs.get('page_id', '')
        self._screen_name = kwargs.get('screen_name', '')
        self._redirect_url = kwargs.get('redirect_url', _router.current_url())

        self._css += ' widget-fb-oauth'

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def access_token_type(self) -> str:
        return self._access_token_type

    @property
    def access_token_expires(self) -> str:
        return self._access_token_expires

    @property
    def user_id(self) -> str:
        return self._user_id

    @property
    def pages(self) -> tuple:
        return tuple(self._pages)

    @property
    def page_id(self) -> str:
        return self._page_id

    @property
    def screen_name(self) -> str:
        return self._screen_name

    def get_html_em(self, **kwargs) -> _html.Element:
        """Get HTML element representation of the widget.
        :param **kwargs:
        """
        # 'state' and 'code' typically received after successful Facebook authorization redirect
        inp = _router.request().inp
        state = inp.get('state')
        auth_code = inp.get('code')

        # Try to fetch access token from Facebook
        if not self._access_token and (state and auth_code):
            t_info = _AuthSession(state).get_access_token(auth_code)
            self._access_token = t_info['access_token']
            self._access_token_type = t_info['token_type']

            self._access_token_expires = float(t_info.get('expires_in', 0))
            if self._access_token_expires:
                self._access_token_expires = int(_datetime.now().timestamp() + self._access_token_expires)

            me = _Session(self._access_token).me()
            self._user_id = me['id']
            self._screen_name = me['name']

        # Pages
        if self._access_token:
            for acc in _Session(self._access_token).accounts():
                if 'CREATE_CONTENT' in acc['perms']:
                    self._pages.append((acc['id'], acc['name']))

        # Link to user profile or to FB authorization URL
        if self._user_id and self._screen_name:
            a = _html.A(self._screen_name, href='https://facebook.com/' + self._user_id, target='_blank')
            a.append(_html.I(cls='fa fa-facebook-square'))
        else:
            a = _html.A(href=_AuthSession(redirect_uri=self._redirect_url).get_authorization_url(self._scope))
            a.append(_html.Img(src=_assetman.url('pytsite.fb@img/facebook-login-button.png')))

        container = _widget.Container(self.uid)
        container.add_widget(_widget.static.Text(
            self.uid + '[auth_url]',
            weight=10,
            label=_lang.t('pytsite.fb@user'), title=a.render()
        ))

        # Page select
        if self.pages:
            container.add_widget(_widget.select.Select(
                self.uid + '[page_id]',
                weight=20,
                value=self._page_id,
                label=_lang.t('pytsite.fb@page'),
                items=self.pages,
                h_size='col-sm-6'
            ))

        container.add_widget(_widget.input.Hidden(self.uid + '[access_token]', value=self.access_token))
        container.add_widget(_widget.input.Hidden(self.uid + '[access_token_type]', value=self.access_token_type))
        container.add_widget(_widget.input.Hidden(self.uid + '[access_token_expires]', value=self.access_token_expires))
        container.add_widget(_widget.input.Hidden(self.uid + '[user_id]', value=self.user_id))
        container.add_widget(_widget.input.Hidden(self.uid + '[screen_name]', value=self.screen_name))

        return self._group_wrap(container.get_html_em())


class Comments(_widget.Base):
    """Facebook Comments Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._href = kwargs.get('href', _router.current_url())

        js_sdk_args = {
            'app_id': _reg.get('fb.app_id'),
            'language': _lang.ietf_tag(sep='_')
        }
        _assetman.add_inline(_tpl.render('pytsite.fb@fb-js-sdk', js_sdk_args))

    def get_html_em(self, **kwargs) -> _html.Element:
        """Get an HTML element representation of the widget.
        :param **kwargs:
        """
        return _html.Div(
                uid=self.uid,
                cls='fb-comments',
                data_href=self._href,
                data_width='100%'
        )

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
        self._access_token = kwargs.get('access_token')
        self._access_token_type = kwargs.get('access_token_type')
        self._access_token_expires = kwargs.get('access_token_expires')
        self._user_id = kwargs.get('user_id')
        self._page_id = kwargs.get('page_id')
        self._screen_name = kwargs.get('screen_name')

        self._css += ' widget-fb-oauth'

        _assetman.add('pytsite.fb@js/widget.js')

    def get_html_em(self) -> _html.Element:
        """Get HTML element representation of the widget.
        """
        # 'state' and 'code' typically received after successful Facebook authorization redirect
        state = _router.request.inp.get('state')
        auth_code = _router.request.inp.get('code')
        if state and auth_code:
            t_info = _AuthSession(state).get_access_token(auth_code)
            self._access_token = t_info['access_token']
            self._access_token_type = t_info['token_type']

            self._access_token_expires = float(t_info.get('expires_in', 0))
            if self._access_token_expires:
                self._access_token_expires = int(_datetime.now().timestamp() + self._access_token_expires)

            me = _Session(self._access_token).me()
            self._user_id = me['id']
            self._screen_name = me['name']

        if self._user_id and self._screen_name:
            a = _html.A(self._screen_name, href='https://facebook.com/' + self._user_id, target='_blank')
            a.append(_html.I(cls='fa fa-facebook-square'))
        else:
            a = _html.A(href=_AuthSession().get_authorization_url(self._scope))
            a.append(_html.Img(src=_assetman.url('pytsite.fb@img/facebook-login-button.png')))

        container = _widget.static.Container(uid='facebook-auth-widget')
        container.append(_widget.static.Text('user', label=_lang.t('pytsite.fb@user'), title=a.render()))

        # Page select
        if self._access_token:
            items = []
            for acc in _Session(self._access_token).accounts():
                if 'CREATE_CONTENT' in acc['perms']:
                    items.append((acc['id'], acc['name']))
            p_select = _widget.select.Select('fb-page-id', name='{}[{}]'.format(self._uid, 'page_id'),
                                             value=self._page_id, label=_lang.t('pytsite.fb@page'), items=items,
                                             h_size='col-sm-6')
            container.append(p_select)

        container.append(_widget.input.Hidden('access-token', name='{}[{}]'.format(self._uid, 'access_token'),
                                              value=self._access_token))
        container.append(_widget.input.Hidden('access-token-type', name='{}[{}]'.format(self._uid, 'access_token_type'),
                                              value=self._access_token_type))
        container.append(_widget.input.Hidden('access-token-expires',
                                              name='{}[{}]'.format(self._uid, 'access_token_expires'),
                                              value=self._access_token_expires))
        container.append(_widget.input.Hidden('user-id', name='{}[{}]'.format(self._uid, 'user_id'),
                                              value=self._user_id))
        container.append(_widget.input.Hidden('screen-name', name='{}[{}]'.format(self._uid, 'screen_name'),
                                              value=self._screen_name))
        container.append(_widget.input.Hidden('title', name='{}[{}]'.format(self._uid, 'title'),
                                              value=self._screen_name))

        return self._group_wrap(container.get_html_em())


class Comments(_widget.Base):
    """Facebook Comments Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        js_sdk_args = {
            'app_id': _reg.get('fb.app_id'),
            'language': _lang.ietf_tag(sep='_')
        }
        _assetman.add_inline(_tpl.render('pytsite.fb@fb-js-sdk', js_sdk_args))

    def get_html_em(self) -> _html.Element:
        """Get an HTML element representation of the widget.
        """
        return _html.Div(
                uid=self.uid,
                cls='fb-comments',
                data_href=_router.current_url(),
                data_width='100%'
        )

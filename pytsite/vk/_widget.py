"""VK Auth Widget.
"""
from pytsite import widget as _widget, html as _html, lang as _lang, router as _router, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Auth(_widget.Abstract):
    """VK oAuth Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._app_id = _settings.get('vk.app_id')
        if not self._app_id:
            raise RuntimeError("Settings parameter 'vk.app_id' is not defined.")

        self._scope = kwargs.get('scope', ('wall', 'offline', 'photos'))
        self._access_url = kwargs.get('access_url', '')
        self._access_token = kwargs.get('access_token', '')
        self._user_id = kwargs.get('user_id', '')
        self._group_id = kwargs.get('group_id', '')

        self._css += ' widget-vk-oauth'

    @property
    def scope(self) -> tuple:
        return self._scope

    @property
    def access_url(self) -> str:
        return self._access_url

    @property
    def group_id(self) -> str:
        return self._group_id

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render widget.
        :param **kwargs:
        """
        authorize_url = _router.url('https://oauth.vk.com/authorize', query={
            'client_id': self._app_id,
            'scope': ','.join(self.scope),
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'response_type': 'token',
            'v': '5.37',
        })

        wrapper = _widget.Container(self.uid)

        wrapper.add_widget(_widget.input.Text(
            uid=self.uid + '[access_url]',
            weight=10,
            label=_lang.t('pytsite.vk@access_url'),
            help=_lang.t('pytsite.vk@access_url_help', {'link': authorize_url}),
            value=self.access_url,
            required=True,
        ))

        wrapper.add_widget(_widget.input.Integer(
            uid=self.uid + '[group_id]',
            weight=20,
            label=_lang.t('pytsite.vk@group_id'),
            value=self.group_id,
            h_size='col-sm-2'
        ))

        return self._group_wrap(wrapper)

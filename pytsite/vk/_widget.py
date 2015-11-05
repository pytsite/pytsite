"""VK Auth Widget.
"""
from pytsite import widget as _widget, html as _html, lang as _lang, assetman as _assetman, router as _router, \
    reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Auth(_widget.Base):
    """Twitter oAuth Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._css += ' widget-vk-oauth'
        self._scope = kwargs.get('scope', ('wall', 'offline', 'photos'))
        self._access_url = kwargs.get('access_url', '')
        self._access_token = kwargs.get('access_token', '')
        self._user_id = kwargs.get('user_id', '')
        self._group_id = kwargs.get('group_id', '')

        _assetman.add('pytsite.vk@js/widget.js')

    def get_html_em(self) -> _html.Element:
        """Render widget.
        """
        authorize_url = _router.url('https://oauth.vk.com/authorize', query={
            'client_id': _reg.get('vk.app_id'),
            'scope': ','.join(self._scope),
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'response_type': 'token',
            'v': '5.37',
        })

        wrapper = _html.TagLessElement()

        wrapper.append(_widget.input.Text(
            weight=10,
            uid='access_url',
            name='{}[access_url]'.format(self._uid),
            label=_lang.t('pytsite.vk@access_url'),
            help=_lang.t('pytsite.vk@access_url_help', {'link': authorize_url}),
            value=self._access_url,
        ).get_html_em())

        wrapper.append(_widget.input.Integer(
            weight=20,
            uid='group_id',
            name='{}[group_id]'.format(self._uid),
            label=_lang.t('pytsite.vk@group_id'),
            value=self._group_id,
            h_size='col-sm-2'
        ).get_html_em())

        wrapper.append(_widget.input.Hidden(
            uid='access_token',
            name='{}[access_token]'.format(self._uid),
            value=self._access_token,
        ).get_html_em())

        wrapper.append(_widget.input.Hidden(
            uid='user_id',
            name='{}[user_id]'.format(self._uid),
            value=self._user_id,
        ).get_html_em())

        return self._group_wrap(wrapper)

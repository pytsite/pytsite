"""Reddit Auth Widget.
"""
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import widget as _widget, html as _html, lang as _lang, assetman as _assetman, router as _router
from ._session import Session as RedditSession, AuthSession as RedditAuthSession

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
        self._access_token = kwargs.get('access_token', '')
        self._access_token_type = kwargs.get('access_token_type', '')
        self._access_token_expires = kwargs.get('access_token_expires', '')
        self._access_token_scope = kwargs.get('access_token_scope', '')
        self._refresh_token = kwargs.get('refresh_token', '')
        self._screen_name = kwargs.get('screen_name', '')

        _assetman.add('pytsite.reddit@js/widget.js')

        self._css += ' widget-reddit-oauth'

    def render(self) -> _html.Element:
        """Render widget.
        """
        # If 'code' is here, we need to exchange it to an access token
        auth_state = _router.request.values_dict.get('state')
        auth_code = _router.request.values_dict.get('code')
        error = _router.request.values_dict.get('error')
        if auth_code and auth_state and not error:
            access_data = RedditAuthSession(auth_state).get_access_token(auth_code)
            self._access_token = access_data['access_token']
            self._access_token_type = access_data['token_type']
            self._access_token_expires = int(_datetime.now().timestamp() + float(access_data['expires_in']))
            self._access_token_scope = access_data['scope']
            self._refresh_token = access_data['refresh_token']
            self._screen_name = RedditSession(self._access_token).user_info()['name']

        wrapper = _html.TagLessElement()
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'access_token'),
                                   value=self._access_token))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'access_token_type'),
                                   value=self._access_token_type))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'access_token_expires'),
                                   value=self._access_token_expires))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'access_token_scope'),
                                   value=self._access_token_scope))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'refresh_token'),
                                   value=self._refresh_token))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'screen_name'),
                                   value=self._screen_name))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'title'),
                                   value=self._screen_name))

        if self._access_token and self._screen_name:
            pass
            a = '<a href="http://reddit.com/user/{}" target="_blank"><i class="fa fa-fw fa-reddit"></i>&nbsp;{}</a>'.\
                format(self._screen_name, self._screen_name)
            wrapper.append(_widget.static.Text(title=a).render())
            #
            # user_info = RedditSession(self._oauth_token, self._oauth_token_secret).user_info()
            # blogs = [(i['name'], i['title']) for i in user_info['blogs']]
            # blog_select = _widget.select.Select(name='{}[{}]'.format(self._uid, 'user_blog'), h_size='col-sm-6',
            #                                     items=blogs, value=self._user_blog, required=True,
            #                                     label=_lang.t('pytsite.tumblr@blog'))
            # wrapper.append(blog_select.render())
        else:
            auth_s = RedditAuthSession()
            wrapper.append(
                _html.A(_lang.t('pytsite.reddit@authorization'), href=auth_s.get_authorization_url())
                    .append(_html.I(cls='fa fa-fw fa-reddit'))
            )

        return self._group_wrap(wrapper)

"""Tumblr Auth Widget.
"""
from pytsite import widget as _widget, html as _html, lang as _lang, assetman as _assetman, router as _router
from ._session import Session as TumblrSession, AuthSession as TumblrAuthSession

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
        self._oauth_token = kwargs.get('oauth_token', '')
        self._oauth_token_secret = kwargs.get('oauth_token_secret', '')
        self._screen_name = kwargs.get('screen_name', '')
        self._user_blog = kwargs.get('user_blog', '')

        _assetman.add('pytsite.tumblr@js/widget.js')

        self._css += ' widget-tumblr-oauth'

    def render(self) -> _html.Element:
        """Render widget.
        """
        # If 'verifier' is here, we need to exchange it to an access token
        inp_oauth_token = _router.request.values_dict.get('oauth_token')
        inp_oauth_verifier = _router.request.values_dict.get('oauth_verifier')
        if inp_oauth_token and inp_oauth_verifier:
            access_data = TumblrAuthSession(inp_oauth_token).get_access_token(_router.current_url())
            self._oauth_token = access_data['oauth_token']
            self._oauth_token_secret = access_data['oauth_token_secret']
            user_info = TumblrSession(self._oauth_token, self._oauth_token_secret).user_info()
            self._screen_name = user_info['name']

        wrapper = _html.TagLessElement()
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'oauth_token'),
                                   value=self._oauth_token))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'oauth_token_secret'),
                                   value=self._oauth_token_secret))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'screen_name'),
                                   value=self._screen_name))
        wrapper.append(_html.Input(type='hidden', name='{}[{}]'.format(self._uid, 'title'),
                                   value=self._screen_name))

        if self._oauth_token and self._oauth_token_secret and self._screen_name:
            a = '<a href="http://{}.tumblr.com" target="_blank"><i class="fa fa-fw fa-tumblr"></i>&nbsp;{}</a>'.\
                format(self._screen_name, self._screen_name)
            wrapper.append(_widget.static.Text(title=a).render())

            user_info = TumblrSession(self._oauth_token, self._oauth_token_secret).user_info()
            blogs = [(i['name'], i['title']) for i in user_info['blogs']]
            blog_select = _widget.select.Select(name='{}[{}]'.format(self._uid, 'user_blog'), h_size='col-sm-6',
                                                items=blogs, value=self._user_blog, required=True,
                                                label=_lang.t('pytsite.tumblr@blog'))
            wrapper.append(blog_select.render())
        else:
            auth_s = TumblrAuthSession(callback_uri=_router.current_url()).fetch_request_token()
            wrapper.append(
                _html.A(_lang.t('pytsite.tumblr@authorization'), href=auth_s.get_authorization_url())
                    .append(_html.I(cls='fa fa-fw fa-tumblr'))
            )

        return self._group_wrap(wrapper)

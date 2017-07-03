"""PytSite Auth Profile Widgets
"""
from pytsite import widget as _widget, tpl as _tpl, auth as _auth, html as _html

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Profile(_widget.Abstract):
    """User Profile Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.

        :type user: pytsite.auth._model.AbstractUser
        """
        super().__init__(uid, **kwargs)

        self._user = kwargs.get('user')
        if not self._user:
            raise ValueError('User is not specified')

        if 'tpl' in kwargs:
            self._tpl = kwargs['tpl']
        elif _tpl.tpl_exists('auth/widget/profile'):
            self._tpl = 'auth/widget/profile'
        else:
            self._tpl = 'pytsite.auth_profile@widget/profile'

        self._css += ' widget-auth-ui-profile'
        self._col_image_css = kwargs.get('col_image_css', 'col-xs-12 col-sm-4 col-md-3 col-lg-2 text-center')
        self._col_content_css = kwargs.get('col_content_css', 'col-xs-12 col-sm-8 col-md-9 col-lg-10')
        self._following_enabled = kwargs.get('following_enabled', True)
        self._js_module = 'pytsite-auth-widget-profile'

        current_user = _auth.get_current_user()
        if not self._user.profile_is_public:
            self._hidden = current_user.login != self._user.login and not current_user.is_admin

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        current_user = _auth.get_current_user()

        # Hidden profiles are visible only for owners and administrators
        if self._hidden:
            return _html.TagLessElement()

        # Rendering widget's template
        content = _html.TagLessElement(_tpl.render(self._tpl, {
            'user': self._user,
            'profile_is_editable': current_user == self._user or current_user.is_admin,
            'col_image_css': self._col_image_css,
            'col_content_css': self._col_content_css,
            'following_enabled': self._following_enabled,
            'follow_button': Follow(uid='auth-ui-follow-widget', user=self._user) if self._following_enabled else None,
        }))

        return content


class Follow(_widget.Abstract):
    """Follow Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.

        :type user: pytsite.auth._model.AbstractUser
        """
        super().__init__(uid, **kwargs)

        self._user = kwargs.get('user')  # type: _auth.model.AbstractUser
        if not self._user:
            raise ValueError('User is not specified.')

        self._current_user = _auth.get_current_user()
        self._tpl = kwargs.get('tpl', 'pytsite.auth_profile@widget/follow')
        self._css += ' inline'

        self._data['follow-msg-id'] = kwargs.get('follow_msg_id', 'pytsite.auth_profile@follow')
        self._data['unfollow-msg-id'] = kwargs.get('unfollow_msg_id', 'pytsite.auth_profile@unfollow')
        self._data['following-msg-id'] = 'pytsite.auth_profile@following'
        self._data['user-id'] = str(self._user.uid)
        self._js_module = 'pytsite-auth-widget-follow'

    def _get_element(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        # Don't show the widget to unauthorized and profile owners
        if self._current_user.is_anonymous or self._current_user == self._user:
            return _html.TagLessElement()

        content = _tpl.render(self._tpl, {
            'current_user': _auth.get_current_user(),
            'user': self._user,
            'follow_msg_id': self._data['follow-msg-id'],
            'unfollow_msg_id': self._data['unfollow-msg-id'],
            'following_msg_id': self._data['following-msg-id'],
        })

        return _html.TagLessElement(content)

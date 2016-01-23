"""Auth UI Widgets.
"""
from pytsite import auth as _auth, widget as _widget, html as _html, tpl as _tpl, odm as _odm, assetman as _assetman
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Profile(_widget.Base):
    """User Profile Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.

        :type user: pytsite.auth._model.User | pytsite.auth_ui._model.UserUI
        """
        super().__init__(uid, **kwargs)

        self._user = kwargs.get('user')
        if not self._user:
            raise ValueError('User is not specified.')

        self._tpl = kwargs.get('tpl', 'pytsite.auth_ui@widget/profile')
        self._css += ' widget-auth-ui-profile'
        self._col_image_css = kwargs.get('col_image_css', 'col-xs-B-12 col-xs-4 col-sm-3 col-lg-2 text-center')
        self._col_content_css = kwargs.get('col_content_css', 'col-xs-B-12 col-xs-8 col-sm-9 col-lg-10')

        _assetman.add('pytsite.auth_ui@css/widget/profile.css')

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        current_user = _auth.get_current_user()

        # Hidden profiles are visible only for owners and administrators
        if not self._user.profile_is_public and current_user.id != self._user.id and not current_user.is_admin:
            return _html.TagLessElement()

        # Check whether to show 'Edit' button
        profile_is_editable = False
        if not current_user.is_anonymous:
            if current_user.id == self._user.id or current_user.has_permission('pytsite.odm_ui.modify.user'):
                profile_is_editable = True

        # Rendering widget's template
        content = _html.TagLessElement(_tpl.render(self._tpl, {
            'user': self._user,
            'profile_is_editable': profile_is_editable,
            'col_image_css': self._col_image_css,
            'col_content_css': self._col_content_css,
        }))

        return self._group_wrap(content)


class Follow(_widget.Base):
    """Follow Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.

        :type user: pytsite.auth._model.User|pytsite.auth_ui._model.UserUI
        """
        super().__init__(uid, **kwargs)

        self._user = kwargs.get('user')
        if not self._user:
            raise ValueError('User is not specified.')

        self._current_user = _auth.get_current_user()
        self._tpl = kwargs.get('tpl', 'pytsite.auth_ui@widget/follow')
        self._follow_msg_id = kwargs.get('follow_msg_id', 'pytsite.auth_ui@follow')
        self._unfollow_msg_id = kwargs.get('unfollow_msg_id', 'pytsite.auth_ui@unfollow')
        self._following_msg_id = 'pytsite.auth_ui@following'

        _assetman.add('pytsite.auth_ui@css/widget/follow.css')
        _assetman.add('pytsite.auth_ui@js/widget/follow.js')

    def get_html_em(self) -> _html.Element:
        """Render the widget.
        """
        # Don't show the widget to unauthorized and profile owners
        if self._current_user.is_anonymous or self._current_user == self._user:
            return _html.TagLessElement()

        content = _tpl.render(self._tpl, {
            'current_user': _auth.get_current_user(),
            'user': self._user,
            'follow_msg_id': self._follow_msg_id,
            'unfollow_msg_id': self._unfollow_msg_id,
            'following_msg_id': self._following_msg_id,
        })

        return _html.TagLessElement(content)


class UserSelect(_widget.select.Select):
    """User Select Widget.
    """
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        f = _auth.find_users().sort([('first_name', _odm.I_ASC)])

        current_user = _auth.get_current_user()
        if not current_user.has_permission('pytsite.odm_ui.browse.user'):
            f.where('login', '=', current_user.login)

        for user in f.get():
            self._items.append(('user:' + str(user.id), '{} ({})'.format(user.full_name, user.login)))

    def set_val(self, value, **kwargs):
        if isinstance(value, _auth.model.User):
            value = 'user:' + str(value.id)

        return super().set_val(value, **kwargs)

    def get_val(self, **kwargs) -> _auth.model.User:
        value = super().get_val(**kwargs)
        if value:
            value = _odm.get_by_ref(value)
            if isinstance(value, _auth.model.User):
                return value
        else:
            return None

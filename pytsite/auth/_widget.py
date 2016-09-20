"""Auth UI Widgets.
"""
from typing import Union as _Union, List as _List, Tuple as _Tuple
from pytsite import widget as _widget, html as _html, tpl as _tpl, assetman as _assetman, lang as _lang
from . import _model, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class RoleCheckboxes(_widget.select.Checkboxes):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        items = [(role.uid, _lang.t(role.description)) for role in _api.get_roles() if role.name != 'anonymous']

        super().__init__(uid, items=items, **kwargs)

    def set_val(self, value: _Union[_List, _Tuple], **kwargs):
        """Set value of the widget.
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError('List or tuple expected.')

        clean_value = []
        for role in value:
            if isinstance(role, _model.AbstractRole):
                clean_value.append(role.uid)
            elif isinstance(role, str):
                clean_value.append(role)
            else:
                raise TypeError('List of roles or UIDs expected.')

        super().set_val(clean_value, **kwargs)


class UserSelect(_widget.select.Select):
    """User Select Widget.
    """
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        c_user = _api.get_current_user()
        if not c_user.is_admin:
            self._items.append((c_user.uid, '{} ({})'.format(c_user.full_name, c_user.login)))
        else:
            for user in _api.get_users({'status': 'active'}, sort_field='first_name'):
                self._items.append((user.uid, '{} ({})'.format(user.full_name, user.login)))

    def set_val(self, value, **kwargs):
        if isinstance(value, _model.AbstractUser):
            value = value.uid
        elif isinstance(value, str):
            # Check user existence
            _api.get_user(uid=value)
        elif value is not None:
            raise TypeError('User object, UID or None expected, got {}.'.format(value))

        return super().set_val(value, **kwargs)

    def get_val(self, **kwargs) -> _model.AbstractUser:
        value = super().get_val(**kwargs)
        if value:
            value = _api.get_user(uid=value)

        return value


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
            raise ValueError('User is not specified.')

        if 'tpl' in kwargs:
            self._tpl = kwargs['tpl']
        elif _tpl.tpl_exists('app@auth/widget/profile'):
            self._tpl = 'app@auth/widget/profile'
        else:
            self._tpl = 'pytsite.auth@widget/profile'

        self._css += ' widget-auth-ui-profile'
        self._col_image_css = kwargs.get('col_image_css', 'col-xs-12 col-sm-4 col-md-3 col-lg-2 text-center')
        self._col_content_css = kwargs.get('col_content_css', 'col-xs-12 col-sm-8 col-md-9 col-lg-10')
        self._following_enabled = kwargs.get('following_enabled', True)

        _assetman.add('pytsite.auth@css/widget/profile.css')

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        current_user = _api.get_current_user()

        # Hidden profiles are visible only for owners and administrators
        if not self._user.profile_is_public and current_user.login != self._user.login and not current_user.is_admin:
            return _html.TagLessElement()

        # Check whether to show 'Edit' button
        profile_is_editable = False
        if current_user.login == self._user.login or current_user.is_admin:
            profile_is_editable = True

        # Rendering widget's template
        content = _html.TagLessElement(_tpl.render(self._tpl, {
            'user': self._user,
            'profile_is_editable': profile_is_editable,
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

        self._user = kwargs.get('user')  # type: _model.AbstractUser
        if not self._user:
            raise ValueError('User is not specified.')

        self._current_user = _api.get_current_user()
        self._tpl = kwargs.get('tpl', 'pytsite.auth@widget/follow')
        self._css += ' inline'

        self._data['follow-msg-id'] = kwargs.get('follow_msg_id', 'pytsite.auth@follow')
        self._data['unfollow-msg-id'] = kwargs.get('unfollow_msg_id', 'pytsite.auth@unfollow')
        self._data['following-msg-id'] = 'pytsite.auth@following'
        self._data['user-id'] = str(self._user.uid)

        self._assets.extend([
            'pytsite.auth@css/widget/follow.css',
            'pytsite.auth@js/widget/follow.js',
        ])

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        # Don't show the widget to unauthorized and profile owners
        if self._current_user.is_anonymous or self._current_user == self._user:
            return _html.TagLessElement()

        content = _tpl.render(self._tpl, {
            'current_user': _api.get_current_user(),
            'user': self._user,
            'follow_msg_id': self._data['follow-msg-id'],
            'unfollow_msg_id': self._data['unfollow-msg-id'],
            'following_msg_id': self._data['following-msg-id'],
        })

        return _html.TagLessElement(content)

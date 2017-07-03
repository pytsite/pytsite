"""PytSite Auth UI Widgets
"""
from typing import Union as _Union, List as _List, Tuple as _Tuple
from pytsite import widget as _widget, lang as _lang
from pytsite.auth import _model, _api

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

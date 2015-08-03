"""Auth UI Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import auth as _auth
from pytsite.core import widget as _widget, html as _html, tpl as _tpl, reg as _reg


class Profile(_widget.Base):
    """User Profile Widget.
    """
    def __init__(self, profile_owner: _auth.model.User, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._profile_owner = profile_owner
        self._group_cls += ' widget-auth-ui-profile'

    def render(self) -> _html.Element:
        """Render the widget.
        """
        modify_button = False
        current_user = _auth.get_current_user()
        if not current_user.is_anonymous:
            if current_user.id == self._profile_owner.id or current_user.has_permission('pytsite.odm_ui.modify.user'):
                modify_button = True

        tpl_name = _reg.get('auth.tpl.profile_view', 'pytsite.auth_ui@profile_widget')
        wrapper = _html.TagLessElement(_tpl.render(tpl_name, {
            'user': self._profile_owner, 'modify_button': modify_button
        }))

        return self._group_wrap(wrapper)

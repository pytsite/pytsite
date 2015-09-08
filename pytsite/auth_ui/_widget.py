"""Auth UI Widgets.
"""
from pytsite import auth as _auth, widget as _widget, html as _html, tpl as _tpl, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Profile(_widget.Base):
    """User Profile Widget.
    """
    def __init__(self, user, tpl: str='pytsite.auth_ui@widget/profile', **kwargs):
        """Init.

        :type user: pytsite.auth._model.User|pytsite.auth_ui._model.UserUI
        """
        super().__init__(**kwargs)
        self._user = user
        self._tpl = tpl
        self._group_cls += ' widget-auth-ui-profile'

    def render(self) -> _html.Element:
        """Render the widget.
        """
        if not self._user.profile_is_public:
            return ''

        profile_is_editable = False
        current_user = _auth.get_current_user()
        if not current_user.is_anonymous:
            if current_user.id == self._user.id or current_user.has_permission('pytsite.odm_ui.modify.user'):
                profile_is_editable = True

        wrapper = _html.TagLessElement(_tpl.render(self._tpl, {
            'user': self._user,
            'profile_is_editable': profile_is_editable
        }))

        return self._group_wrap(wrapper)

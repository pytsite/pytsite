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
        self._css += ' widget-auth-ui-profile'
        self._col_image_css = kwargs.get('col_image_css', 'col-xs-B-12 col-xs-4 col-sm-3 col-lg-2 text-center')
        self._col_content_css = kwargs.get('col_content_css', 'col-xs-B-12 col-xs-8 col-sm-9 col-lg-10')

    def render(self) -> _html.Element:
        """Render the widget.
        """
        current_user = _auth.get_current_user()

        # Hidden profiles are visible only for owners and administrators
        if not self._user.profile_is_public and current_user.id != self._user.id and not current_user.is_admin:
            return ''

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

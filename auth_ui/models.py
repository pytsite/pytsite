"""ODM UI Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widget.input import TextInputWidget
from pytsite.auth.models import User
from pytsite.odm_ui.models import ODMUIMixin


class UserUI(User, ODMUIMixin):

    def get_permission_group(self) -> str:
        """Get permission group name.
        """
        return 'auth'

    def get_lang_package(self) -> str:
        """Get language package name.
        """
        return 'pytsite.auth_ui'

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.head_columns = 'login', 'email', 'last_login',

    def get_browser_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return self.f_get('login'), self.f_get('email'), self.f_get('lastLogin', fmt='%x %X')

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.form.AbstractForm
        """
        form.add_widget(TextInputWidget(
            uid='login',
            value=self.f_get('login'),
            label=self.t('login'),
        ), 10)

        form.add_widget(TextInputWidget(
            uid='email',
            value=self.f_get('email'),
            label=self.t('email'),
        ), 20)

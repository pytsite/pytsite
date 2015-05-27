"""ODM UI Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widgets.input import TextInputWidget
from pytsite.core.validation.rules import NotEmptyRule, EmailRule, ODMRefsListRule
from pytsite.auth.models import User
from pytsite.odm_ui.models import ODMUIMixin
from pytsite.odm_ui.widgets import EntityCheckboxesWidget
from pytsite.file.widgets import FilesUploadWidget


class UserUI(User, ODMUIMixin):
    """User UI.
    """

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
        browser.data_fields = 'login', 'email', 'last_login'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return self.f_get('login'), self.f_get('email'), self.f_get('lastLogin', fmt='%x %X')

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.form.BaseForm
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

        form.add_widget(EntityCheckboxesWidget(
            uid='roles',
            label=self.t('roles'),
            model='role',
            caption_field='description'
        ), 30)

        form.add_widget(FilesUploadWidget(
            uid='picture',
            label=self.t('picture'),
            model='image',
        ), 40)

        form.add_rules('login', (NotEmptyRule(), EmailRule()))
        form.add_rules('email', (NotEmptyRule(), EmailRule()))
        form.add_rules('roles', (NotEmptyRule(),))

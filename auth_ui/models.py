"""ODM UI Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widgets.input import *
from pytsite.core.widgets.selectable import *
from pytsite.core.widgets.static import *
from pytsite.core.validation.rules import NotEmptyRule, EmailRule
from pytsite.core.odm.validation import ODMEntitiesListRule
from pytsite.auth import auth_manager
from pytsite.auth.models import User
from pytsite.odm_ui.models import ODMUIMixin
from pytsite.odm_ui.widgets import EntityCheckboxesWidget
from pytsite.image.widgets import ImagesUploadWidget


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
        return self.f_get('login'), self.f_get('email'), self.f_get('last_login', fmt='%x %X')

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.forms.BaseForm
        """

        form.add_widget(CheckboxWidget(
            uid='profile_is_public',
            value=self.f_get('profile_is_public'),
            label=self.t('profile_is_public'),
        ), 10)

        form.add_widget(TextInputWidget(
            uid='login',
            value=self.f_get('login'),
            label=self.t('login'),
        ), 20)

        form.add_widget(TextInputWidget(
            uid='email',
            value=self.f_get('email'),
            label=self.t('email'),
        ), 30)

        form.add_widget(TextInputWidget(
            uid='full_name',
            value=self.f_get('full_name'),
            label=self.t('name'),
        ), 40)

        form.add_widget(SelectWidget(
            uid='status',
            value=self.f_get('status'),
            label=self.t('status'),
            items=auth_manager.get_user_statuses(),
            h_size='col-sm-5 col-md-4 col-lg-3',
        ), 50)

        form.add_widget(ImagesUploadWidget(
            uid='picture',
            label=self.t('picture'),
            value=self.f_get('picture'),
            max_files=1,
            max_file_size=1,
        ), 60)

        form.add_widget(EntityCheckboxesWidget(
            uid='roles',
            label=self.t('roles'),
            model='role',
            caption_field='description',
            value=self.f_get('roles'),
        ), 70)

        form.add_widget(StaticTextWidget(
            uid='token',
            value=self.f_get('token'),
            label=self.t('token'),
        ), 80)

        form.add_rules('login', (NotEmptyRule(), EmailRule()))
        form.add_rules('email', (NotEmptyRule(), EmailRule()))
        form.add_rules('roles', (NotEmptyRule(), ODMEntitiesListRule(model='role'),))

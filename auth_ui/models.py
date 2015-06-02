"""ODM UI Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widgets.input import *
from pytsite.core.widgets.selectable import *
from pytsite.core.widgets.static import *
from pytsite.core.validation.rules import NotEmptyRule, EmailRule
from pytsite.core.odm.validation import ODMEntitiesListRule, ODMFieldUniqueRule
from pytsite.core.html import Span, Div, Input, Label
from pytsite.auth import auth_manager
from pytsite.auth.models import User, Role
from pytsite.odm_ui.models import ODMUIMixin
from pytsite.odm_ui.widgets import EntityCheckboxesWidget
from pytsite.image.widgets import ImagesUploadWidget
from pytsite.core.lang import t


class UserUI(User, ODMUIMixin):
    """User UI.
    """

    def get_permission_group(self) -> tuple:
        """Get permission group spec.
        """
        return 'auth', 'pytsite.auth_ui@security'

    def get_lang_package(self) -> str:
        """Get language package name.
        """
        return 'pytsite.auth_ui'

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = 'login', 'email', 'status', 'last_login'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return (
            self.f_get('login'),
            self.f_get('email'),
            t('pytsite.auth@status_'+self.f_get('status')),
            self.f_get('last_login', fmt='%x %X')
        )

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

        if not self.is_new:
            form.add_widget(StaticControlWidget(
                uid='token',
                value=self.f_get('token'),
                label=self.t('token'),
            ), 80)

        form.add_rules('login', (NotEmptyRule(), EmailRule(), ODMFieldUniqueRule('user', 'login', (self.id,))))
        form.add_rules('email', (NotEmptyRule(), EmailRule()))
        form.add_rules('roles', (NotEmptyRule(), ODMEntitiesListRule(model='role')))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('login')


class RoleUI(Role, ODMUIMixin):
    """Role UI.
    """

    def get_permission_group(self) -> tuple:
        """Get permission group spec.
        """
        return 'auth', 'pytsite.auth_ui@security'

    def get_lang_package(self) -> str:
        return 'pytsite.auth_ui'

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = 'name', 'description', 'permissions'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        perms = []
        for perm_name in self.f_get('permissions'):
            perm = auth_manager.get_permission(perm_name)
            cls = 'label label-default permission-' + perm[0]
            if perm[0] == 'admin':
                cls += ' label-danger'
            perms.append(str(Span(t(perm[1]), cls=cls)))

        return (
            self.f_get('name'),
            t(self.f_get('description')),
            ' '.join(perms)
        )

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.forms.BaseForm
        """

        form.add_widget(TextInputWidget(
            uid='name',
            value=self.f_get('name'),
            label=self.t('name'),
        ), 10)

        form.add_widget(TextInputWidget(
            uid='description',
            value=self.f_get('description'),
            label=self.t('description'),
        ), 20)

        perms_tabs = TabsWidget(uid='permissions', label=self.t('permissions'))
        for group in auth_manager.get_permission_groups():
            tab_content = Div()
            for perm in auth_manager.get_permissions(group[0]):
                p_name = perm[0]
                tab_content.append(
                    Div(cls='checkbox').append(
                        Label(t(perm[1]), label_for='permissions-checkbox-' + p_name).append(
                            Input(type='checkbox', uid='permissions-checkbox-' + p_name,
                                  name='permissions', value=p_name, checked=p_name in self.f_get('permissions'))
                        )
                    )
                )
            perms_tabs.add_tab('permissions-' + group[0], t(group[1]), tab_content.render())

        form.add_widget(HiddenInputWidget(name='permissions', value=''))
        form.add_widget(perms_tabs, 30)

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return t(self.f_get('description'))

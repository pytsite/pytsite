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
from pytsite.core.lang import t
from pytsite.core.http.errors import ForbiddenError
from pytsite.auth import auth_manager
from pytsite.auth.models import User, Role
from pytsite.odm_ui.models import ODMUIMixin
from pytsite.odm_ui.widgets import ODMCheckboxesWidget
from pytsite.image.widgets import ImagesUploadWidget


class UserUI(User, ODMUIMixin):
    """User UI.
    """

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = 'login', 'email', 'roles', 'status', 'last_login'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        groups_cell = ''
        for g in self.f_get('roles'):
            cls = 'label label-default'
            if g.f_get('name') == 'admin':
                cls += ' label-danger'
            groups_cell += str(Span(t(g.f_get('description')), cls=cls)) + ' '

        return (
            self.f_get('login'),
            self.f_get('email'),
            groups_cell,
            t('pytsite.auth@status_'+self.f_get('status')),
            self.f_get('last_login', fmt='%x %X')
        )

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.forms.BaseForm
        """

        form.add_widget(CheckboxWidget(
            weight=10,
            uid='profile_is_public',
            value=self.f_get('profile_is_public'),
            label=self.t('profile_is_public'),
        ))

        form.add_widget(TextInputWidget(
            weight=20,
            uid='login',
            value=self.f_get('login'),
            label=self.t('login'),
        ))

        form.add_widget(TextInputWidget(
            weight=30,
            uid='email',
            value=self.f_get('email'),
            label=self.t('email'),
        ))

        form.add_widget(TextInputWidget(
            weight=40,
            uid='full_name',
            value=self.f_get('full_name'),
            label=self.t('name'),
        ))

        form.add_widget(SelectWidget(
            weight=50,
            uid='status',
            value=self.f_get('status'),
            label=self.t('status'),
            items=auth_manager.get_user_statuses(),
            h_size='col-sm-5 col-md-4 col-lg-3',
        ))

        form.add_widget(ImagesUploadWidget(
            weight=60,
            uid='picture',
            label=self.t('picture'),
            value=self.f_get('picture'),
            max_files=1,
            max_file_size=1,
            image_max_width=256,
            image_max_height=256,
        ))

        form.add_widget(ODMCheckboxesWidget(
            weight=70,
            uid='roles',
            label=self.t('roles'),
            model='role',
            caption_field='description',
            value=self.f_get('roles'),
        ))

        if not self.is_new:
            form.add_widget(StaticControlWidget(
                weight=80,
                uid='token',
                value=self.f_get('token'),
                label=self.t('token'),
            ))

        form.add_rules('login', (NotEmptyRule(), EmailRule(), ODMFieldUniqueRule('user', 'login', (self.id,))))
        form.add_rules('email', (NotEmptyRule(), EmailRule()))
        form.add_rules('roles', (ODMEntitiesListRule(model='role'),))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('login')


class RoleUI(Role, ODMUIMixin):
    """Role UI.
    """

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = 'name', 'description', 'permissions'

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        if self.f_get('name') == 'admin':
            return

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
        if self.f_get('name') == 'admin':
            raise ForbiddenError()

        form.add_widget(TextInputWidget(
            weight=10,
            uid='name',
            value=self.f_get('name'),
            label=self.t('name'),
        ))

        form.add_widget(TextInputWidget(
            weight=20,
            uid='description',
            value=self.f_get('description'),
            label=self.t('description'),
        ))

        perms_tabs = TabsWidget(weight=30, uid='permissions', label=self.t('permissions'))
        for group in auth_manager.get_permission_groups():
            if group[0] == 'auth':
                continue

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
        form.add_widget(perms_tabs)

        form.add_rules('name', (NotEmptyRule(),))
        form.add_rules('description', (NotEmptyRule(),))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        if self.f_get('name') == 'admin':
            raise ForbiddenError()

        return t(self.f_get('description'))

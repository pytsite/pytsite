"""ODM UI Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import core as _core, auth as _auth, odm_ui as _odm_ui, image as _image

class UserUI(_auth.model.User, _auth.model.ODMUIMixin):
    """User UI.
    """

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.ODMUIBrowser
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
            groups_cell += str(_core.html.Span(_core.lang.t(g.f_get('description')), cls=cls)) + ' '

        return (
            self.f_get('login'),
            self.f_get('email'),
            groups_cell,
            _core.lang.t('pytsite.auth@status_'+self.f_get('status')),
            self.f_get('last_login', fmt='%x %X')
        )

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.form.Base
        """
        form.add_widget(_core.widget.select.Checkbox(
            weight=10,
            uid='profile_is_public',
            value=self.f_get('profile_is_public'),
            label=self.t('profile_is_public'),
        ))

        form.add_widget(_core.widget.input.Text(
            weight=20,
            uid='login',
            value=self.f_get('login'),
            label=self.t('login'),
        ))
        form.add_rules('login', (
            _core.validation.rule.NotEmpty(),
            _core.validation.rule.Email(),
            _core.odm.validation.ODMFieldUnique('user', 'login', (self.id,))
        ))

        form.add_widget(_core.widget.input.Text(
            weight=30,
            uid='email',
            value=self.f_get('email'),
            label=self.t('email'),
        ))
        form.add_rules('email', (_core.validation.rule.NotEmpty(), _core.validation.rule.Email()))

        form.add_widget(_core.widget.input.Text(
            weight=40,
            uid='full_name',
            value=self.f_get('full_name'),
            label=self.t('name'),
        ))

        form.add_widget(_core.widget.select.Select(
            weight=50,
            uid='status',
            value=self.f_get('status'),
            label=self.t('status'),
            items=_auth.manager.get_user_statuses(),
            h_size='col-sm-5 col-md-4 col-lg-3',
        ))

        form.add_widget(_image.widget.ImagesUploadWidget(
            weight=60,
            uid='picture',
            label=self.t('picture'),
            value=self.f_get('picture'),
            max_files=1,
            max_file_size=1,
            image_max_width=256,
            image_max_height=256,
        ))

        form.add_widget(_odm_ui.widget.ODMCheckboxes(
            weight=70,
            uid='roles',
            label=self.t('roles'),
            model='role',
            caption_field='description',
            value=self.f_get('roles'),
        ))
        form.add_rules('roles', (_core.odm.validation.ODMEntitiesList(model='role'),))

        if not self.is_new:
            form.add_widget(_core.widget.input.Text(
                weight=80,
                uid='token',
                value=self.f_get('token'),
                label=self.t('token'),
            ))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('login')


class RoleUI(_auth.model.Role, _odm_ui.model.ODMUIMixin):
    """Role UI.
    """

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.ODMUIBrowser
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
            perm = _auth.manager.get_permission(perm_name)
            cls = 'label label-default permission-' + perm[0]
            if perm[0] == 'admin':
                cls += ' label-danger'
            perms.append(str(_core.html.Span(_core.lang.t(perm[1]), cls=cls)))

        return (
            self.f_get('name'),
            _core.lang.t(self.f_get('description')),
            ' '.join(perms)
        )

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.form.Base
        """
        if self.f_get('name') == 'admin':
            raise _core.http.error.ForbiddenError()

        form.add_widget(_core.widget.input.Text(
            weight=10,
            uid='name',
            value=self.f_get('name'),
            label=self.t('name'),
        ))

        form.add_widget(_core.widget.input.Text(
            weight=20,
            uid='description',
            value=self.f_get('description'),
            label=self.t('description'),
        ))

        perms_tabs = _core.widget.static.Tabs(weight=30, uid='permissions', label=self.t('permissions'))
        for group in _auth.manager.get_permission_groups():
            if group[0] == 'auth':
                continue

            tab_content = _core.html.Div()
            for perm in _auth.manager.get_permissions(group[0]):
                p_name = perm[0]
                tab_content.append(
                    _core.html.Div(cls='checkbox').append(
                        _core.html.Label(_core.lang.t(perm[1]), label_for='permissions-checkbox-' + p_name).append(
                            _core.html.Input(type='checkbox', uid='permissions-checkbox-' + p_name,
                                  name='permissions', value=p_name, checked=p_name in self.f_get('permissions'))
                        )
                    )
                )
            perms_tabs.add_tab('permissions-' + group[0], _core.lang.t(group[1]), tab_content.render())

        form.add_widget(_core.widget.input.Hidden(name='permissions', value=''))
        form.add_widget(perms_tabs)

        form.add_rules('name', (_core.validation.rule.NotEmpty(),))
        form.add_rules('description', (_core.validation.rule.NotEmpty(),))

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        if self.f_get('name') == 'admin':
            raise _core.http.error.ForbiddenError()

        return _core.lang.t(self.f_get('description'))
"""PytSite Authorization ODM Storage Models.
"""
import hashlib as _hashlib
from typing import Iterable as _Iterable, Tuple as _Tuple, List as _List, Union as _Union
from datetime import datetime as _datetime
from pytsite import auth as _auth, odm as _odm, util as _util, odm_ui as _odm_ui, router as _router, \
    html as _html, widget as _widget, form as _form, lang as _lang, metatag as _metatag, validation as _validation, \
    admin as _admin, permission as _permission, http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Role(_auth.model.RoleInterface, _odm_ui.model.UIEntity):
    @property
    def name(self) -> str:
        return self.f_get('name')

    @name.setter
    def name(self, value: str):
        self.f_set('name', value)

    @property
    def description(self) -> str:
        return self.f_get('description')

    @description.setter
    def description(self, value: str):
        self.f_set('description', value)

    @property
    def permissions(self) -> _Iterable[str]:
        return self.f_get('permissions')

    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('name'))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.UniqueStringList('permissions'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('name', _odm.I_ASC)], unique=True)

    def _pre_delete(self, **kwargs):
        """Hook.
        """
        # Check if the role is used by users
        for user in _auth.get_users(False):
            if user.has_role(self.name):
                raise _odm.error.ForbidEntityDelete(self.t('role_used_by_user', {'user': user.login}))

    @classmethod
    def ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = 'name', 'description', 'permissions'

    def ui_browser_get_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        if self.f_get('name') == 'admin':
            return

        perms = []
        for perm_name in self.f_get('permissions'):
            if not _permission.is_permission_defined(perm_name):
                continue
            perm = _permission.get_permission(perm_name)
            cls = 'label label-default permission-' + perm[0]
            if perm[0] == 'admin':
                cls += ' label-danger'
            perms.append(str(_html.Span(_lang.t(perm[1]), cls=cls)))

        return self.f_get('name'), _lang.t(self.f_get('description')), ' '.join(perms)

    def ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        if self.name == 'admin':
            raise _http.error.Forbidden()

    def ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        frm.add_widget(_widget.input.Text(
            weight=10,
            uid='name',
            value=self.name,
            label=self.t('name'),
            required=True,
        ))

        frm.add_widget(_widget.input.Text(
            weight=20,
            uid='description',
            value=self.description,
            label=self.t('description'),
            required=True,
        ))

        # Permissions tabs
        perms_tabs = _widget.static.Tabs('permissions-tabs', weight=30, label=self.t('permissions'))
        for g_name, g_desc in sorted(_permission.get_permission_groups().items(), key=lambda x: x[0]):
            if g_name == 'auth':
                continue

            tab_content = _html.Div()
            for perm in _permission.get_permissions(g_name):
                p_name = perm[0]
                tab_content.append(
                    _html.Div(cls='checkbox').append(
                        _html.Label(_lang.t(perm[1]), label_for='permissions-checkbox-' + p_name).append(
                            _html.Input(type='checkbox', uid='permissions-checkbox-' + p_name,
                                        name='permissions', value=p_name, checked=p_name in self.permissions)
                        )
                    )
                )
            perms_tabs.add_tab('permissions-' + g_name, _lang.t(g_desc), tab_content.render())

        frm.add_widget(_widget.input.Hidden('permissions', value=''))
        frm.add_widget(perms_tabs)

    def ui_mass_action_get_entity_description(self) -> str:
        """Get delete form description.
        """
        return _lang.t(self.description)


class User(_auth.model.UserInterface, _odm_ui.model.UIEntity):
    @property
    def uid(self) -> str:
        return str(self.id)

    @property
    def is_new(self) -> bool:
        return _odm.model.Entity.is_new.fget(self)

    @property
    def created(self) -> bool:
        return self.f_get('_created')

    @property
    def login(self) -> str:
        return self.f_get('login')

    @login.setter
    def login(self, value: str):
        self.f_set('login', value)

    @property
    def email(self) -> str:
        return self.f_get('email')

    @email.setter
    def email(self, value: str):
        self.f_set('email', value)

    @property
    def password(self) -> str:
        return self.f_get('password')

    @password.setter
    def password(self, value: str):
        self.f_set('password', value)

    @property
    def nickname(self) -> str:
        return self.f_get('nickname')

    @nickname.setter
    def nickname(self, value: str):
        self.f_set('nickname', value)

    @property
    def access_token(self) -> str:
        return self.f_get('access_token')

    @access_token.setter
    def access_token(self, value: str):
        self.f_set('access_token', value)

    @property
    def first_name(self) -> str:
        return self.f_get('first_name')

    @first_name.setter
    def first_name(self, value: str):
        self.f_set('first_name', value)

    @property
    def last_name(self) -> str:
        return self.f_get('last_name')

    @last_name.setter
    def last_name(self, value: str):
        self.f_set('last_name', value)

    @property
    def description(self) -> str:
        return self.f_get('description')

    @description.setter
    def description(self, value: str):
        self.f_set('description', value)

    @property
    def birth_date(self) -> _datetime:
        return self.f_get('birth_date')

    @birth_date.setter
    def birth_date(self, value: _datetime):
        self.f_set('birth_date', value)

    @property
    def last_sign_in(self) -> _datetime:
        return self.f_get('last_sign_in')

    @last_sign_in.setter
    def last_sign_in(self, value: _datetime):
        self.f_set('last_sign_in', value)

    @property
    def last_activity(self) -> _datetime:
        return self.f_get('last_activity')

    @last_activity.setter
    def last_activity(self, value: _datetime):
        self.f_set('last_activity', value)

    @property
    def sign_in_count(self) -> int:
        return self.f_get('sign_in_count')

    @sign_in_count.setter
    def sign_in_count(self, value: int):
        self.f_set('sign_in_count', value)

    @property
    def status(self) -> bool:
        return self.f_get('status')

    @status.setter
    def status(self, value: str):
        self.f_set('status', value)

    @property
    def roles(self) -> _Tuple[Role]:
        try:
            return super().roles
        except NotImplementedError:
            return self.f_get('roles')

    @roles.setter
    def roles(self, value: tuple):
        self.f_set('roles', value)

    @property
    def gender(self) -> str:
        return self.f_get('gender')

    @gender.setter
    def gender(self, value: str):
        self.f_set('gender', value)

    @property
    def phone(self) -> int:
        return self.f_get('phone')

    @phone.setter
    def phone(self, value: int):
        self.f_set('phone', value)

    @property
    def options(self) -> dict:
        return self.f_get('options')

    @options.setter
    def options(self, value: dict):
        self.f_set('options', value)

    @property
    def picture(self):
        """
        :rtype: pytsite.image.model.Image
        """
        return self.f_get('picture')

    @picture.setter
    def picture(self, value):
        self.f_set('picture', value)

    @property
    def urls(self) -> tuple:
        return self.f_get('urls')

    @urls.setter
    def urls(self, value: tuple):
        self.f_set('urls', value)

    @property
    def profile_is_public(self) -> bool:
        return self.f_get('profile_is_public')

    @profile_is_public.setter
    def profile_is_public(self, value: bool):
        self.f_set('profile_is_public', value)

    @property
    def follows(self):
        """
        :return: _Iterable[User]
        """
        return self.f_get('follows')

    @follows.setter
    def follows(self, value):
        self.f_set('follows', value)

    @property
    def followers(self):
        """
        :return: _Iterable[User]
        """
        return self.f_get('followers')

    @followers.setter
    def followers(self, value):
        self.f_set('followers', value)

    @property
    def last_ip(self) -> str:
        return self.f_get('last_ip')

    @last_ip.setter
    def last_ip(self, value: str):
        self.f_set('last_ip', value)

    @property
    def country(self) -> str:
        return self.f_get('country')

    @country.setter
    def country(self, value: str):
        self.f_set('country', value)

    @property
    def city(self) -> str:
        return self.f_get('city')

    @city.setter
    def city(self, value: str):
        self.f_set('city', value)

    def _setup_fields(self):
        """_setup() hook.
        """
        # Fields
        self.define_field(_odm.field.String('login', nonempty=True))
        self.define_field(_odm.field.String('email', nonempty=True))
        self.define_field(_odm.field.String('password', nonempty=True))
        self.define_field(_odm.field.String('nickname', nonempty=True))
        self.define_field(_odm.field.String('access_token'))
        self.define_field(_odm.field.Bool('profile_is_public', default=False))
        self.define_field(_odm.field.String('first_name'))
        self.define_field(_odm.field.String('last_name'))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.DateTime('birth_date'))
        self.define_field(_odm.field.DateTime('last_sign_in'))
        self.define_field(_odm.field.DateTime('last_activity'))
        self.define_field(_odm.field.Integer('sign_in_count'))
        self.define_field(_odm.field.String('status', default='active'))
        self.define_field(_odm.field.RefsUniqueList('roles', model='role'))
        self.define_field(_odm.field.String('gender'))
        self.define_field(_odm.field.String('phone'))
        self.define_field(_odm.field.Dict('options'))
        self.define_field(_odm.field.Ref('picture', model='image'))
        self.define_field(_odm.field.StringList('urls', unique=True))
        self.define_field(_odm.field.RefsUniqueList('follows', model='user'))
        self.define_field(_odm.field.RefsUniqueList('followers', model='user'))
        self.define_field(_odm.field.String('last_ip'))
        self.define_field(_odm.field.String('country'))
        self.define_field(_odm.field.String('city'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('login', _odm.I_ASC)], unique=True)
        self.define_index([('nickname', _odm.I_ASC)], unique=True)
        self.define_index([('access_token', _odm.I_ASC)])
        self.define_index([('last_sign_in', _odm.I_DESC)])

    def storage_save(self):
        _odm.model.Entity.save(self)

    def storage_delete(self):
        _odm.model.Entity.delete(self)

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'password':
            if value:
                value = _auth.hash_password(value)
            else:
                if self.is_new:
                    # Set random password
                    value = _auth.hash_password(_util.random_password())
                else:
                    # Keep old password
                    value = self.password

        if field_name == 'status':
            if value not in [v[0] for v in _auth.get_user_statuses()]:
                raise RuntimeError("Invalid user status: '{}'.".format(value))

        if field_name == 'nickname':
            value = self._sanitize_nickname(value)

        return value

    def _sanitize_nickname(self, s: str) -> str:
        """Generate unique nickname.
        """
        cnt = 0
        s = _util.transform_str_2(s[:32])
        nickname = s
        while True:
            try:
                user = _auth.get_user(nickname=nickname)

                # If nickname of THIS user was not changed
                if user == self:
                    return s

            except _auth.error.UserNotExist:
                return nickname

            cnt += 1
            nickname = s + '-' + str(cnt)

    def _pre_save(self):
        """Hook.
        """
        if self.is_anonymous:
            raise RuntimeError('Anonymous user cannot be saved.')

        if self.is_system:
            raise RuntimeError('System user cannot be saved.')

        if not self.password:
            self.password = ''

        if not self.nickname:
            m = _hashlib.md5()
            m.update(self.login.encode('UTF-8'))
            self.nickname = m.hexdigest()

    def _pre_delete(self, **kwargs):
        """Hook.
        """
        # Users cannot delete themselves
        if _auth.get_current_user() == self and self.is_admin:
            raise _odm.error.ForbidEntityDelete(self.t('you_cannot_delete_yourself'))

        # Search for entities which user owns
        for model in _odm.get_registered_models():
            for entity in _odm.find(model).get():
                for f_name in ('author', 'owner'):
                    if entity.has_field(f_name) and entity.f_get(f_name) == self:
                        # Skip user's avatar to avoid  deletion block
                        if model == 'image' and self.picture == entity:
                            continue

                        raise _odm.error.ForbidEntityDelete(
                            self.t('account_owns_entity', {'entity': entity.model + ':' + str(entity.id)}))

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'full_name':
            value = self.first_name
            if self.last_name:
                value += ' ' + self.last_name

        return value

    def as_dict(self, fields: _Union[_List, _Tuple] = (), **kwargs):
        # Never show user's password
        r = super().as_dict([f for f in fields if f != 'password'], **kwargs)

        if 'geo_ip' in r:
            r['geo_ip'] = self.geo_ip.as_dict(('ip', 'asn', 'city', 'country', 'country_code', 'isp', 'longitude',
                                               'latitude', 'location', 'organization', 'postal_code', 'region',
                                               'region_name', 'timezone'))

        return r

    @classmethod
    def ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = 'login', 'full_name', 'roles', 'status', 'profile_is_public', 'is_online', '_created', \
                              'last_activity'
        browser.default_sort_field = 'last_activity'

    def ui_view_url(self) -> str:
        return _router.ep_url('pytsite.auth@profile_view', {'nickname': self.nickname})

    def ui_browser_get_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        roles_cell = ''
        for role in sorted(self.f_get('roles'), key=lambda role: role.name):
            cls = 'label label-default'
            if role.name == 'admin':
                cls += ' label-danger'
            roles_cell += str(_html.Span(_lang.t(role.description), cls=cls)) + ' '

        status_cls = 'info' if self.status == 'active' else 'default'

        return (
            '<a href="' + self.url + '">' + self.login + '</a>',
            self.full_name,
            roles_cell,
            '<span class="label label-{}">{}</span>'.format(status_cls,
                                                            _lang.t('pytsite.auth@status_' + self.f_get('status'))),
            '<span class="label label-info">{}</span>'.format(self.t('word_yes')) if self.profile_is_public else '',
            '<span class="label label-success">{}</span>'.format(self.t('word_yes')) if self.is_online else '',
            self.f_get('_created', fmt='pretty_date_time'),
            self.f_get('last_activity', fmt='pretty_date_time')
        )

    def ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        if not _router.current_path().startswith(_admin.base_path()):
            frm.redirect = 'ENTITY_VIEW'

        frm.area_footer_css += ' text-center'
        frm.area_body_css += ' row'

        _metatag.t_set('title', self.t('profile_edit'))

    def ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        current_user = _auth.get_current_user()

        # Picture wrapper
        pic_wrapper = _widget.Container(
            uid='picture-wrapper',
            weight=2,
            css='col-xs-12 col-sm-4 col-lg-3',
        )
        frm.add_widget(pic_wrapper)

        # Content wrapper
        content_wrapper = _widget.Container(
            uid='content-wrapper',
            weight=4,
            css='col-xs-12 col-sm-8 col-lg-9',
        )
        frm.add_widget(content_wrapper)

        # Image
        from pytsite import image
        pic_wrapper.add_widget(image.widget.ImagesUpload(
            weight=10,
            uid='picture',
            value=self.picture,
            max_file_size=1,
            show_numbers=False,
            dnd=False,
            slot_css='col-xs-B-12 col-xs-6 col-sm-12',
        ))

        # Profile is public
        content_wrapper.add_widget(_widget.select.Checkbox(
            weight=10,
            uid='profile_is_public',
            value=self.f_get('profile_is_public'),
            label=self.t('profile_is_public'),
        ))

        # Login
        if current_user.has_permission('pytsite.odm_perm.modify.user'):
            content_wrapper.add_widget(_widget.input.Email(
                weight=30,
                uid='login',
                value=self.login,
                label=self.t('login'),
                required=True,
            ))
            frm.add_rule('login', _odm.validation.FieldUnique(
                'pytsite.auth@this_login_already_used',
                model='user',
                field='login',
                exclude_ids=self.id
            ))

        # Nickname
        content_wrapper.add_widget(_widget.input.Text(
            weight=40,
            uid='nickname',
            value=self.nickname,
            label=self.t('nickname'),
            required=True,
        ))
        frm.add_rules('nickname', (
            _auth.user_nickname_rule,
            _odm.validation.FieldUnique(
                msg_id='pytsite.auth@this_nickname_already_used',
                model=self.model,
                field='nickname',
                exclude_ids=self.id
            )
        ))

        # First name
        content_wrapper.add_widget(_widget.input.Text(
            weight=50,
            uid='first_name',
            value=self.first_name,
            label=self.t('first_name'),
            required=True,
        ))

        # Last name
        content_wrapper.add_widget(_widget.input.Text(
            weight=60,
            uid='last_name',
            value=self.last_name,
            label=self.t('last_name'),
        ))

        # Email
        content_wrapper.add_widget(_widget.input.Email(
            weight=70,
            uid='email',
            value=self.f_get('email'),
            label=self.t('email'),
            required=True,
        ))
        frm.add_rule('email', _odm.validation.FieldUnique(
            msg_id='pytsite.auth@this_email_already_used',
            model=self.model,
            field='email',
            exclude_ids=self.id
        ))

        # Password
        content_wrapper.add_widget(_widget.input.Password(
            weight=80,
            uid='password',
            label=self.t('password'),
        ))

        # Country
        content_wrapper.add_widget(_widget.input.Text(
            weight=90,
            uid='country',
            label=self.t('country'),
            value=self.country,
        ))

        # City
        content_wrapper.add_widget(_widget.input.Text(
            weight=100,
            uid='city',
            label=self.t('city'),
            value=self.city,
        ))

        # Description
        content_wrapper.add_widget(_widget.input.TextArea(
            weight=110,
            uid='description',
            value=self.f_get('description'),
            label=self.t('about_yourself'),
            max_length=1024,
        ))

        # Status
        if current_user.has_permission('pytsite.odm_perm.modify.user'):
            content_wrapper.add_widget(_widget.select.Select(
                weight=120,
                uid='status',
                value=self.f_get('status'),
                label=self.t('status'),
                items=_auth.get_user_statuses(),
                h_size='col-sm-5 col-md-4 col-lg-3',
                required=True,
            ))

        # URLs
        content_wrapper.add_widget(_widget.input.StringList(
            weight=130,
            uid='urls',
            label=self.t('social_links'),
            value=self.urls,
            max_values=5,
            add_btn_label=self.t('add_link'),
        ))
        frm.add_rule('urls', _validation.rule.Url())

        # Roles
        if current_user.has_permission('pytsite.odm_perm.modify.user'):
            content_wrapper.add_widget(_odm_ui.widget.EntityCheckboxes(
                weight=140,
                uid='roles',
                label=self.t('roles'),
                model='role',
                caption_field='description',
                exclude=(_auth.get_role('anonymous'),),
                value=self.f_get('roles'),
            ))
            frm.add_rule('roles', _odm.validation.ODMEntitiesList(model='role'))

        # Token
        if not self.is_new and current_user.has_permission('pytsite.odm_perm.modify.user'):
            content_wrapper.add_widget(_widget.input.Text(
                weight=150,
                uid='access_token',
                value=self.access_token,
                label=self.t('token'),
            ))
            frm.add_rules('access_token', (
                _validation.rule.Regex(pattern='^[a-f0-9]{32}$'),
                _odm.validation.FieldUnique(
                    msg_id='pytsite.auth@this_token_already_used',
                    model=self.model,
                    field='access_token',
                    exclude_ids=self.id)
            ))

    def get_profile_edit_form(self) -> _form.Form:
        return _odm_ui.get_m_form('user', str(self.id))

    def ui_mass_action_get_entity_description(self) -> str:
        """Get delete form description.
        """
        return self.login

    def perm_check(self, action: str) -> bool:
        # Users can modify themselves
        user = _auth.get_current_user()
        if action == 'modify' and not user.is_anonymous and user == self:
            return True

        return super().perm_check(action)

    def add_follower(self, follower: _auth.model.UserInterface):
        self.f_add('followers', follower)

    def remove_follower(self, follower: _auth.model.UserInterface):
        self.f_sub('followers', follower)

    def add_follows(self, user: _auth.model.UserInterface):
        self.f_add('follows', user)

    def remove_follows(self, user: _auth.model.UserInterface):
        self.f_sub('follows', user)

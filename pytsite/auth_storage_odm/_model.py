"""PytSite Authorization ODM Storage Models.
"""
import hashlib as _hashlib
from typing import Tuple as _Tuple
from datetime import datetime as _datetime
from pytsite import auth as _auth, odm as _odm, util as _util, odm_ui as _odm_ui, router as _router, \
    html as _html, widget as _widget, form as _form, lang as _lang, metatag as _metatag, validation as _validation, \
    permission as _permission, http as _http, image as _image, events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Role(_auth.model.AbstractRole, _odm_ui.model.UIEntity):
    @property
    def uid(self) -> str:
        return str(self.id)

    @property
    def is_new(self) -> bool:
        return _odm_ui.model.UIEntity.is_new.fget(self)

    @property
    def name(self) -> str:
        return self.f_get('name')

    @name.setter
    def name(self, value: str):
        with self:
            self.f_set('name', value)

    @property
    def description(self) -> str:
        return self.f_get('description')

    @description.setter
    def description(self, value: str):
        with self:
            self.f_set('description', value)

    @property
    def permissions(self) -> _Tuple[str]:
        try:
            return super().permissions
        except NotImplementedError:
            return self.f_get('permissions')

    @permissions.setter
    def permissions(self, value: _Tuple[str]):
        with self:
            self.f_set('permissions', value)

    def save(self):
        is_new = self.is_new

        if is_new:
            _events.fire('pytsite.auth.role.pre_create', role=self)

        _events.fire('pytsite.auth.role.pre_save', role=self)

        with self:
            _odm_ui.model.UIEntity.save(self)

        _events.fire('pytsite.auth.role.save', role=self)

        if is_new:
            _events.fire('pytsite.auth.role.create', role=self)

        return self

    def delete(self):
        _events.fire('pytsite.auth.role.pre_delete', role=self)

        with self:
            _odm_ui.model.UIEntity.delete(self)

        _events.fire('pytsite.auth.role.delete', role=self)

        return self

    @classmethod
    def get_permission_group(cls) -> str:
        return 'security'

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
        for user in _auth.get_users():
            if user.has_role(self.name):
                raise _odm.error.ForbidEntityDelete(self.t('role_used_by_user', {'user': user.login}))

    @classmethod
    def ui_browser_setup(cls, browser: _odm_ui.Browser):
        browser.data_fields = [
            ('name', 'pytsite.auth_storage_odm@name'),
            ('description', 'pytsite.auth_storage_odm@description'),
            ('permissions', 'pytsite.auth_storage_odm@permissions', False),
        ]

        browser.default_sort_field = 'name'

    def ui_browser_get_row(self) -> tuple:
        if self.name == 'admin':
            return

        perms = []
        for perm_name in self.permissions:
            # If permission was renamed or deleted (sometimes it happens), juts ignore it
            if not _permission.is_permission_defined(perm_name):
                continue

            perm = _permission.get_permission(perm_name)
            cls = 'label label-default permission-' + perm[0]
            if perm[0] == 'admin':
                cls += ' label-danger'
            perms.append(str(_html.Span(_lang.t(perm[1]), cls=cls)))

        return self.name, _lang.t(self.description), ' '.join(perms)

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


class User(_auth.model.AbstractUser, _odm_ui.model.UIEntity):
    @property
    def uid(self) -> str:
        return str(self.id)

    @property
    def is_new(self) -> bool:
        return _odm_ui.model.UIEntity.is_new.fget(self)

    @property
    def created(self) -> _datetime:
        return self.f_get('_created')

    @property
    def login(self) -> str:
        return self.f_get('login')

    @login.setter
    def login(self, value: str):
        with self:
            self.f_set('login', value)

    @property
    def email(self) -> str:
        return self.f_get('email')

    @email.setter
    def email(self, value: str):
        with self:
            self.f_set('email', value)

    @property
    def password(self) -> str:
        return self.f_get('password')

    @password.setter
    def password(self, value: str):
        with self:
            self.f_set('password', value)

    @property
    def nickname(self) -> str:
        return self.f_get('nickname')

    @nickname.setter
    def nickname(self, value: str):
        with self:
            self.f_set('nickname', value)

    @property
    def access_token(self) -> str:
        return self.f_get('acs_token')

    @access_token.setter
    def access_token(self, value: str):
        with self:
            self.f_set('acs_token', value)

    @property
    def first_name(self) -> str:
        return self.f_get('first_name')

    @first_name.setter
    def first_name(self, value: str):
        with self:
            self.f_set('first_name', value)

    @property
    def last_name(self) -> str:
        return self.f_get('last_name')

    @last_name.setter
    def last_name(self, value: str):
        with self:
            self.f_set('last_name', value)

    @property
    def description(self) -> str:
        return self.f_get('description')

    @description.setter
    def description(self, value: str):
        with self:
            self.f_set('description', value)

    @property
    def birth_date(self) -> _datetime:
        return self.f_get('birth_date')

    @birth_date.setter
    def birth_date(self, value: _datetime):
        with self:
            self.f_set('birth_date', value)

    @property
    def last_sign_in(self) -> _datetime:
        return self.f_get('last_sign_in')

    @last_sign_in.setter
    def last_sign_in(self, value: _datetime):
        with self:
            self.f_set('last_sign_in', value)

    @property
    def last_activity(self) -> _datetime:
        return self.f_get('last_activity')

    @last_activity.setter
    def last_activity(self, value: _datetime):
        with self:
            self.f_set('last_activity', value)

    @property
    def sign_in_count(self) -> int:
        return self.f_get('sign_in_count')

    @sign_in_count.setter
    def sign_in_count(self, value: int):
        with self:
            self.f_set('sign_in_count', value)

    @property
    def status(self) -> str:
        return self.f_get('status')

    @status.setter
    def status(self, value: str):
        with self:
            self.f_set('status', value)

    @property
    def roles(self) -> _Tuple[Role]:
        try:
            return super().roles
        except NotImplementedError:
            return self.f_get('roles')

    @roles.setter
    def roles(self, value: tuple):
        with self:
            self.f_set('roles', value)

    @property
    def gender(self) -> str:
        return self.f_get('gender')

    @gender.setter
    def gender(self, value: str):
        with self:
            self.f_set('gender', value)

    @property
    def phone(self) -> int:
        return self.f_get('phone')

    @phone.setter
    def phone(self, value: int):
        with self:
            self.f_set('phone', value)

    @property
    def options(self) -> dict:
        return self.f_get('options')

    @options.setter
    def options(self, value: dict):
        with self:
            self.f_set('options', value)

    @property
    def picture(self):
        """
        :rtype: pytsite.image.model.Image
        """
        return self.f_get('picture')

    @picture.setter
    def picture(self, value):
        with self:
            self.f_set('picture', value)

    @property
    def urls(self) -> tuple:
        return self.f_get('urls')

    @urls.setter
    def urls(self, value: tuple):
        with self:
            self.f_set('urls', value)

    @property
    def profile_is_public(self) -> bool:
        return self.f_get('profile_is_public')

    @profile_is_public.setter
    def profile_is_public(self, value: bool):
        with self:
            self.f_set('profile_is_public', value)

    @property
    def follows(self):
        """
        :return: _Iterable[User]
        """
        return self.f_get('follows')

    @follows.setter
    def follows(self, value):
        with self:
            self.f_set('follows', value)

    @property
    def followers(self):
        """
        :return: _Iterable[User]
        """
        return self.f_get('followers')

    @followers.setter
    def followers(self, value):
        with self:
            self.f_set('followers', value)

    @property
    def last_ip(self) -> str:
        return self.f_get('last_ip')

    @last_ip.setter
    def last_ip(self, value: str):
        with self:
            self.f_set('last_ip', value)

    @property
    def country(self) -> str:
        return self.f_get('country')

    @country.setter
    def country(self, value: str):
        with self:
            self.f_set('country', value)

    @property
    def city(self) -> str:
        return self.f_get('city')

    @city.setter
    def city(self, value: str):
        with self:
            self.f_set('city', value)

    def save(self):
        is_new = self.is_new

        if is_new:
            _events.fire('pytsite.auth.user.pre_create', user=self)

        _events.fire('pytsite.auth.user.pre_save', user=self)

        # Do actual save into storage
        with self:
            _odm_ui.model.UIEntity.save(self)

        _events.fire('pytsite.auth.user.save', user=self)

        if is_new:
            _events.fire('pytsite.auth.user.create', user=self)

        return self

    def _pre_delete(self, **kwargs):
        if self == _auth.get_current_user():
            raise _odm.error.ForbidEntityDelete(self.t('you_cannot_delete_yourself'))

    def delete(self):
        _events.fire('pytsite.auth.user.pre_delete', user=self)

        with self:
            _odm_ui.model.UIEntity.delete(self)

        _events.fire('pytsite.auth.user.delete', user=self)

        return self

    @classmethod
    def get_permission_group(cls) -> str:
        return 'security'

    def _setup_fields(self):
        """_setup() hook.
        """
        # Fields
        self.define_field(_odm.field.String('login', nonempty=True))
        self.define_field(_odm.field.String('email', nonempty=True))
        self.define_field(_odm.field.String('password', nonempty=True))
        self.define_field(_odm.field.String('nickname', nonempty=True))
        self.define_field(_odm.field.String('acs_token'))
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
        self.define_index([('acs_token', _odm.I_ASC)])
        self.define_index([('last_sign_in', _odm.I_DESC)])

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
        super()._pre_save()

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

    def _after_save(self, first_save: bool = False):
        # Load user picture from Gravatar
        if not self.picture:
            img_url = 'https://www.gravatar.com/avatar/' + _util.md5_hex_digest(self.email) + '?s=512'
            img_owner = self if not self.is_new else _auth.get_first_admin_user()
            self.picture = _image.create(img_url, owner=img_owner)
            self.save()

    def _after_delete(self, **kwargs):
        """Hook.
        """
        if self.picture:
            with self.picture:
                self.picture.delete()

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'full_name':
            value = self.first_name
            if self.last_name:
                value += ' ' + self.last_name

        return value

    def as_jsonable(self, **kwargs):
        return {
            'login': self.login,
        }

    @classmethod
    def ui_browser_setup(cls, browser: _odm_ui.Browser):
        browser.data_fields = [
            ('login', 'pytsite.auth_storage_odm@login'),
            ('full_name', 'pytsite.auth_storage_odm@full_name', False),
            ('roles', 'pytsite.auth_storage_odm@roles', False),
            ('status', 'pytsite.auth_storage_odm@status'),
            ('profile_is_public', 'pytsite.auth_storage_odm@profile_is_public'),
            ('is_online', 'pytsite.auth_storage_odm@is_online'),
            ('created', 'pytsite.auth_storage_odm@created'),
            ('last_activity', 'pytsite.auth_storage_odm@last_activity'),
        ]

        browser.default_sort_field = 'last_activity'
        browser.default_sort_order = 'desc'

    def ui_browser_get_row(self) -> dict:
        yes = _lang.t('pytsite.auth_storage_odm@word_yes')

        login = '<a href="' + self.profile_view_url + '">' + self.login + '</a>'

        roles = ''
        for role in sorted(self.roles, key=lambda role: role.name):
            cls = 'label label-default'
            if role.name == 'admin':
                cls += ' label-danger'
            roles += str(_html.Span(_lang.t(role.description), cls=cls)) + ' '

        status_cls = 'info' if self.status == 'active' else 'default'
        status_word = _lang.t('pytsite.auth@status_' + self.status)
        status = '<span class="label label-{}">{}</span>'.format(status_cls, status_word)

        p_is_public = '<span class="label label-info">{}</span>'.format(yes) if self.profile_is_public else '',
        is_online = '<span class="label label-success">{}</span>'.format(yes) if self.is_online else ''
        created = _lang.pretty_date_time(self.created)
        last_activity = _lang.pretty_date_time(self.last_activity)

        return login, self.full_name, roles, status, p_is_public, is_online, created, last_activity

    def ui_view_url(self) -> str:
        return _router.ep_url('pytsite.auth@profile_view', {'nickname': self.nickname})

    def ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
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
                'pytsite.auth_storage_odm@this_login_already_used',
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
                msg_id='pytsite.auth_storage_odm@this_nickname_already_used',
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
            msg_id='pytsite.auth_storage_odm@this_email_already_used',
            model=self.model,
            field='email',
            exclude_ids=self.id
        ))

        # Password
        content_wrapper.add_widget(_widget.input.Password(
            weight=80,
            uid='password',
            label=self.t('new_password'),
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
                uid='acs_token',
                value=self.access_token,
                label=self.t('token'),
            ))
            frm.add_rules('acs_token', (
                _validation.rule.Regex(pattern='^[a-f0-9]{32}$'),
                _odm.validation.FieldUnique(
                    msg_id='pytsite.auth_storage_odm@this_token_already_used',
                    model=self.model,
                    field='acs_token',
                    exclude_ids=self.id)
            ))

    def ui_mass_action_get_entity_description(self) -> str:
        return '{} ({})'.format(self.login, self.full_name)

    def add_follower(self, follower: _auth.model.AbstractUser):
        with self:
            self.f_add('followers', follower)

    def remove_follower(self, follower: _auth.model.AbstractUser):
        with self:
            self.f_sub('followers', follower)

    def add_follows(self, user: _auth.model.AbstractUser):
        with self:
            self.f_add('follows', user)

    def remove_follows(self, user: _auth.model.AbstractUser):
        with self:
            self.f_sub('follows', user)

    def check_permissions(self, action: str) -> bool:
        # Users can modify themselves
        if action == 'modify' and _auth.get_current_user() == self:
            return True

        return super().check_permissions(action)

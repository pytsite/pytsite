"""PytSite Authorization ODM Storage Models.
"""
import hashlib as _hashlib
from typing import Optional as _Optional, Tuple as _Tuple
from datetime import datetime as _datetime
from pytsite import auth as _auth, odm as _odm, util as _util, odm_ui as _odm_ui, router as _router, \
    html as _html, widget as _widget, form as _form, lang as _lang, metatag as _metatag, validation as _validation, \
    permissions as _permissions, http as _http, file as _file, file_storage_odm as _file_storage_odm, \
    events as _events, errors as _errors
from . import _field

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ODMRole(_odm_ui.model.UIEntity):
    @classmethod
    def odm_auth_permissions_group(cls) -> str:
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

    def _after_save(self, first_save: bool = False, **kwargs):
        super()._after_save(first_save, **kwargs)

        role = _auth.get_role(uid=str(self.id))

        if first_save:
            _events.fire('pytsite.auth.role.create', role=role)

        _events.fire('pytsite.auth.role.save', role=role)

    def _pre_delete(self, **kwargs):
        """Hook.
        """
        # Check if the role is used by users
        for user in _auth.get_users():
            if user.has_role(self.f_get('name')):
                raise _errors.ForbidDeletion(self.t('role_used_by_user', {'user': user.login}))

        _events.fire('pytsite.auth.role.delete', role=_auth.get_role(uid=str(self.id)))

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
        browser.data_fields = [
            ('name', 'pytsite.auth_storage_odm@name'),
            ('description', 'pytsite.auth_storage_odm@description'),
            ('permissions', 'pytsite.auth_storage_odm@permissions', False),
        ]

        browser.default_sort_field = 'name'

    def odm_ui_browser_row(self) -> _Optional[_Tuple]:
        if self.f_get('name') == 'admin':
            return

        perms = []
        for perm_name in self.f_get('permissions'):
            # If permission was renamed or deleted (sometimes it happens), juts ignore it
            if not _permissions.is_permission_defined(perm_name):
                continue

            perm = _permissions.get_permission(perm_name)
            css = 'label label-default permission-' + perm[0]
            if perm[0] == 'admin':
                css += ' label-danger'
            perms.append(str(_html.Span(_lang.t(perm[1]), css=css)))

        return self.f_get('name'), _lang.t(self.f_get('description')), ' '.join(perms)

    def odm_ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        # Admin role cannot be changed
        if self.f_get('name') == 'admin':
            raise _http.error.Forbidden()

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        frm.add_widget(_widget.input.Text(
            weight=10,
            uid='name',
            value=self.f_get('name'),
            label=self.t('name'),
            required=True,
        ))

        frm.add_widget(_widget.input.Text(
            weight=20,
            uid='description',
            value=self.f_get('description'),
            label=self.t('description'),
            required=True,
        ))

        # Permissions tabs
        perms_tabs = _widget.select.Tabs(
            uid='permissions-tabs',
            weight=30,
            label=self.t('permissions')
        )

        # Permissions tabs content
        for g_name, g_desc in sorted(_permissions.get_permission_groups().items(), key=lambda x: x[0]):
            if g_name == 'auth':
                continue

            perms = _permissions.get_permissions(g_name)
            if not perms:
                continue

            # Tab
            tab_id = 'permissions-' + g_name
            perms_tabs.add_tab(tab_id, _lang.t(g_desc))

            # Tab's content
            perms_tabs.append_child(_widget.select.Checkboxes(
                uid='permission-checkboxes-' + tab_id,
                name='permissions',
                items=[(p[0], _lang.t(p[1])) for p in perms],
                value=self.f_get('permissions'),
            ), tab_id)

        frm.add_widget(perms_tabs)

    def odm_ui_mass_action_entity_description(self) -> str:
        """Get delete form description.
        """
        return _lang.t(self.f_get('description'))


class Role(_auth.model.AbstractRole):
    def __init__(self, odm_entity: ODMRole):
        if not isinstance(odm_entity, ODMRole):
            raise TypeError('Instance of ODMRole expected, got {}.'.format(type(odm_entity)))

        self._entity = odm_entity

    @property
    def odm_entity(self) -> ODMRole:
        return self._entity

    @property
    def uid(self) -> str:
        return str(self._entity.id)

    def has_field(self, field_name: str) -> bool:
        return self._entity.has_field(field_name)

    def get_field(self, field_name: str):
        return self._entity.f_get(field_name)

    def set_field(self, field_name: str, value):
        with self._entity as e:
            e.f_set(field_name, value)

        return self

    def save(self):
        with self._entity as e:
            e.save()

        return self

    def delete(self):
        with self._entity as e:
            e.delete()

        return self


class ODMUser(_odm_ui.model.UIEntity):
    """ODM model to store information about user.
    """

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        """Hook.
        """
        return 'security'

    def _setup_fields(self):
        """Hook.
        """
        # Fields
        self.define_field(_odm.field.String('login', required=True))
        self.define_field(_odm.field.String('email', required=True))
        self.define_field(_odm.field.String('password', required=True))
        self.define_field(_odm.field.String('nickname', required=True))
        self.define_field(_odm.field.Bool('profile_is_public', default=False))
        self.define_field(_odm.field.String('first_name'))
        self.define_field(_odm.field.String('last_name'))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.DateTime('birth_date'))
        self.define_field(_odm.field.DateTime('last_sign_in'))
        self.define_field(_odm.field.DateTime('last_activity'))
        self.define_field(_odm.field.Integer('sign_in_count'))
        self.define_field(_odm.field.String('status', default='active'))
        self.define_field(_field.Roles('roles'))
        self.define_field(_odm.field.String('gender'))
        self.define_field(_odm.field.String('phone'))
        self.define_field(_odm.field.Dict('options'))
        self.define_field(_file_storage_odm.field.Image('picture'))
        self.define_field(_odm.field.StringList('urls', unique=True))
        self.define_field(_field.Users('follows'))
        self.define_field(_field.Users('followers'))
        self.define_field(_odm.field.String('last_ip'))
        self.define_field(_odm.field.String('country'))
        self.define_field(_odm.field.String('city'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('login', _odm.I_ASC)], unique=True)
        self.define_index([('nickname', _odm.I_ASC)], unique=True)
        self.define_index([('last_sign_in', _odm.I_DESC)])

    def _on_f_get(self, field_name: str, value, **kwargs):
        if field_name == 'picture' and not self.is_new and not self.get_field('picture').get_val():
            # Load user picture from Gravatar
            img_url = 'https://www.gravatar.com/avatar/' + _util.md5_hex_digest(self.f_get('email')) + '?s=512'
            img = _file.create(img_url)
            with self:
                _auth.switch_user_to_system()
                self.f_set('picture', img).save()
                _auth.restore_user()
            value = img

        return value

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
                    value = self.f_get('password')

        elif field_name == 'status':
            if value not in [v[0] for v in _auth.get_user_statuses()]:
                raise RuntimeError("Invalid user status: '{}'.".format(value))

        elif field_name == 'nickname':
            value = self._sanitize_nickname(value)

        return super()._on_f_set(field_name, value, **kwargs)

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
                if user.nickname == self.f_get('nickname'):
                    return s

            except _auth.error.UserNotExist:
                return nickname

            cnt += 1
            nickname = s + '-' + str(cnt)

    def _pre_save(self, **kwargs):
        """Hook.
        """
        super()._pre_save(**kwargs)

        if not self.f_get('password'):
            self.f_set('password', '')

        if not self.f_get('nickname'):
            m = _hashlib.md5()
            m.update(self.f_get('login').encode('UTF-8'))
            self.f_set('nickname', m.hexdigest())

    def _after_save(self, first_save: bool = False, **kwargs):
        super()._after_save(first_save, **kwargs)

        user = _auth.get_user(uid=str(self.id))

        if first_save:
            _events.fire('pytsite.auth.user.create', user=user)

        _events.fire('pytsite.auth.user.save', user=user)

    def _pre_delete(self, **kwargs):

        super()._pre_delete(**kwargs)

        if str(self.id) == _auth.get_current_user().uid:
            raise _errors.ForbidDeletion(self.t('you_cannot_delete_yourself'))

        _events.fire('pytsite.auth.user.delete', user=_auth.get_user(uid=str(self.id)))

    def _after_delete(self, **kwargs):
        """Hook.
        """
        pic = self.f_get('picture')
        if pic:
            pic.delete()

    @classmethod
    def odm_ui_browser_setup(cls, browser: _odm_ui.Browser):
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

    def odm_ui_browser_row(self) -> _Tuple:
        yes = _lang.t('pytsite.auth_storage_odm@word_yes')

        login = '<a href="' + self.url + '">' + self.f_get('login') + '</a>'

        roles = ''
        for role in sorted(self.f_get('roles'), key=lambda rl: rl.name):
            css = 'label label-default'
            if role.name == 'admin':
                css += ' label-danger'
            roles += str(_html.Span(_lang.t(role.description), css=css)) + ' '

        status_css = 'info' if self.f_get('status') == 'active' else 'default'
        status_word = _lang.t('pytsite.auth@status_' + self.f_get('status'))
        status = '<span class="label label-{}">{}</span>'.format(status_css, status_word)

        p_is_public = '<span class="label label-info">{}</span>'.format(yes) if self.f_get('profile_is_public') else '',
        is_online = '<span class="label label-success">{}</span>'.format(yes) \
            if (_datetime.now() - self.f_get('last_activity')).seconds < 180 else ''
        created = _lang.pretty_date_time(self.created)
        last_activity = _lang.pretty_date_time(self.f_get('last_activity'))
        full_name = self.f_get('first_name') + ' ' + self.f_get('last_name')

        return login, full_name, roles, status, p_is_public, is_online, created, last_activity

    def odm_ui_view_url(self) -> str:
        return _router.ep_url('pytsite.auth@profile_view', {'nickname': self.f_get('nickname')})

    def odm_ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        frm.area_footer_css += ' text-center'
        frm.area_body_css += ' row'

        _metatag.t_set('title', self.t('profile_edit'))

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
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
        pic_wrapper.append_child(_file.widget.ImagesUpload(
            weight=10,
            uid='picture',
            value=self.f_get('picture'),
            max_file_size=1,
            show_numbers=False,
            dnd=False,
            slot_css='col-xs-B-12 col-xs-6 col-sm-12',
        ))

        # Profile is public
        content_wrapper.append_child(_widget.select.Checkbox(
            weight=10,
            uid='profile_is_public',
            value=self.f_get('profile_is_public'),
            label=self.t('profile_is_public'),
        ))

        # Login
        if current_user.has_permission('pytsite.odm_auth.modify.user'):
            content_wrapper.append_child(_widget.input.Email(
                weight=30,
                uid='login',
                value=self.f_get('login'),
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
        content_wrapper.append_child(_widget.input.Text(
            weight=40,
            uid='nickname',
            value=self.f_get('nickname'),
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
        content_wrapper.append_child(_widget.input.Text(
            weight=50,
            uid='first_name',
            value=self.f_get('first_name'),
            label=self.t('first_name'),
            required=True,
        ))

        # Last name
        content_wrapper.append_child(_widget.input.Text(
            weight=60,
            uid='last_name',
            value=self.f_get('last_name'),
            label=self.t('last_name'),
        ))

        # Email
        content_wrapper.append_child(_widget.input.Email(
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
        content_wrapper.append_child(_widget.input.Password(
            weight=80,
            uid='password',
            label=self.t('new_password'),
        ))

        # Country
        content_wrapper.append_child(_widget.input.Text(
            weight=90,
            uid='country',
            label=self.t('country'),
            value=self.f_get('country'),
        ))

        # City
        content_wrapper.append_child(_widget.input.Text(
            weight=100,
            uid='city',
            label=self.t('city'),
            value=self.f_get('city'),
        ))

        # Description
        content_wrapper.append_child(_widget.input.TextArea(
            weight=110,
            uid='description',
            value=self.f_get('description'),
            label=self.t('about_yourself'),
            max_length=1024,
        ))

        # Status
        if current_user.has_permission('pytsite.odm_auth.modify.user'):
            content_wrapper.append_child(_widget.select.Select(
                weight=120,
                uid='status',
                value=self.f_get('status'),
                label=self.t('status'),
                items=_auth.get_user_statuses(),
                h_size='col-sm-5 col-md-4 col-lg-3',
                required=True,
            ))

        # URLs
        content_wrapper.append_child(_widget.input.StringList(
            weight=130,
            uid='urls',
            label=self.t('social_links'),
            value=self.f_get('urls'),
            max_values=5,
            add_btn_label=self.t('add_link'),
        ))
        frm.add_rule('urls', _validation.rule.Url())

        # Roles
        if current_user.has_permission('pytsite.odm_auth.modify.user'):
            content_wrapper.append_child(_auth.widget.RoleCheckboxes(
                weight=140,
                uid='roles',
                label=self.t('roles'),
                value=self.f_get('roles'),
            ))

    def odm_ui_mass_action_entity_description(self) -> str:
        return '{} ({} {})'.format(self.f_get('login'), self.f_get('first_name'), self.f_get('last_name'))

    def odm_auth_check_permission(self, perm: str, user: _auth.model.AbstractUser = None) -> bool:
        if not user:
            user = _auth.get_current_user()

        # Users can modify themselves
        if perm in ('modify', 'modify_own') and user.uid == str(self.id):
            return True

        return super().odm_auth_check_permission(perm, user)


class User(_auth.model.AbstractUser):
    def __init__(self, odm_entity: ODMUser):
        if not isinstance(odm_entity, ODMUser):
            raise TypeError('Instance of ODMUser expected, got {}.'.format(type(odm_entity)))

        self._entity = odm_entity

    @property
    def odm_entity(self) -> ODMUser:
        return self._entity

    @property
    def uid(self) -> str:
        return str(self._entity.id)

    @property
    def created(self) -> str:
        return self.get_field('_created')

    def has_field(self, field_name: str) -> bool:
        return self._entity.has_field(field_name)

    def get_field(self, field_name: str):
        return self._entity.f_get(field_name)

    def set_field(self, field_name: str, value):
        with self._entity as e:
            e.f_set(field_name, value)

        return self

    @property
    def uid(self) -> str:
        return str(self._entity.id)

    def save(self):
        if self.is_anonymous:
            raise RuntimeError('Anonymous user cannot be saved.')

        if self.is_system:
            raise RuntimeError('System user cannot be saved.')

        with self._entity as e:
            e.save()

        return self

    def delete(self):
        with self._entity as e:
            e.delete()

        return self

    def add_role(self, role: _auth.model.AbstractRole):
        with self._entity as e:
            e.f_add('roles', role)

        return self

    def remove_role(self, role: _auth.model.AbstractRole):
        with self._entity as e:
            e.f_sub('roles', role)

        return self

    def add_follower(self, follower: _auth.model.AbstractUser):
        with self._entity as e:
            e.f_add('followers', follower)

        return self

    def remove_follower(self, follower: _auth.model.AbstractUser):
        with self._entity as e:
            e.f_sub('followers', follower)

        return self

    def add_follows(self, user: _auth.model.AbstractUser):
        with self._entity as e:
            e.f_add('follows', user)

        return self

    def remove_follows(self, user: _auth.model.AbstractUser):
        with self._entity as e:
            e.f_sub('follows', user)

        return self

"""Auth Log ODM Models.
"""
from typing import Tuple as _Tuple
from pytsite import odm as _odm, odm_ui as _odm_ui, auth as _auth, geo_ip as _geo_ip, lang as _lang, \
    auth_storage_odm as _auth_storage_odm
from . import _api


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AuthLog(_odm_ui.model.UIEntity):
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_auth_storage_odm.field.User('user'))
        self.define_field(_odm.field.String('ip', required=True))
        self.define_field(_odm.field.Integer('severity', default=_api.SEVERITY_INFO))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.Virtual('geo_ip'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('user', _odm.I_ASC)])
        self.define_index([('ip', _odm.I_ASC)])
        self.define_index([('severity', _odm.I_ASC)])

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        return 'security'

    @classmethod
    def odm_auth_permissions(cls) -> _Tuple[str]:
        return 'delete',

    @property
    def user(self) -> _auth.model.AbstractUser:
        return self.f_get('user')

    @property
    def ip(self) -> str:
        return self.f_get('ip')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def severity(self) -> int:
        return self.f_get('severity')

    @property
    def geo_ip(self) -> _geo_ip.model.GeoIP:
        try:
            return _geo_ip.resolve(self.ip)
        except _geo_ip.error.ResolveError:
            pass

    @classmethod
    def odm_ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.default_sort_field = '_created'
        browser.default_sort_order = 'desc'
        browser.data_fields = [
            ('user', 'pytsite.auth_log@user'),
            ('ip', 'pytsite.auth_log@ip'),
            ('geo_data', 'pytsite.auth_log@geo_data', False),
            ('description', 'pytsite.auth_log@description', False),
            ('severity', 'pytsite.auth_log@severity'),
            ('_created', 'pytsite.auth_log@created'),
        ]

    def odm_ui_browser_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        user = ''
        if self.user:
            user = '<a href="{}">{}</a>'.format(self.user.profile_view_url, self.user.full_name)

        ip = self.ip
        g_ip = self.geo_ip
        geo = '{}, {}'.format(g_ip.country, g_ip.city) if g_ip.country else ''
        description = self.description
        modified = self.f_get('_modified', fmt='pretty_date_time')

        severity_class = 'info'
        severity_name = _lang.t('pytsite.auth_log@severity_info')
        if self.severity == _api.SEVERITY_WARNING:
            severity_class = 'warning'
            severity_name = _lang.t('pytsite.auth_log@severity_warning')
        elif self.severity == _api.SEVERITY_ERROR:
            severity_class = 'warning'
            severity_name = _lang.t('pytsite.auth_log@severity_error')

        severity = '<span class="label label-{}">{}</span>'.format(severity_class, severity_name)

        return user, ip, geo, description, severity, modified

"""Auth Log ODM Models.
"""
from pytsite import odm as _odm, odm_ui as _odm_ui, auth as _auth, geo_ip as _geo_ip, lang as _lang, router as _router
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AuthLog(_odm_ui.UIEntity):
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.Ref('user', model='user'))
        self.define_field(_odm.field.String('ip', nonempty=True))
        self.define_field(_odm.field.Integer('severity', default=_api.SEVERITY_INFO))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.Virtual('geo_ip'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('user', _odm.I_ASC)])
        self.define_index([('ip', _odm.I_ASC)])
        self.define_index([('severity', _odm.I_ASC)])

    @property
    def user(self) -> _auth.model.User:
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
    def ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = ('user', 'ip', 'geo_data', 'description', 'severity', '_created')

    def ui_browser_get_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        user = ''
        if self.user:
            user_edit_url = _router.ep_url('pytsite.odm_ui.ep.m_form', {
                'model': 'user',
                'id': str(self.user.id),
            })
            user = '<a href="{}">{}</a>'.format(user_edit_url, self.user.full_name)

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

    def ui_can_be_created(self) -> bool:
        return False

    def ui_can_be_modified(self) -> bool:
        return False

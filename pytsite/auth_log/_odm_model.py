"""Auth Log ODM Models.
"""
from pytsite import odm as _odm, odm_ui as _odm_ui, auth as _auth, geo_ip as _geo_ip, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AuthLog(_odm_ui.Model):
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
    def geo_ip(self) -> _geo_ip.odm_model.GeoIP:
        try:
            return _geo_ip.resolve(self.ip)
        except _geo_ip.error.ResolveError:
            pass

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = ('user', 'ip', 'geo_data', 'description', 'timestamp')

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        user = self.user.full_name
        ip = self.ip
        g_ip = self.geo_ip
        geo = '{}, {}'.format(g_ip.country, g_ip.city) if g_ip.country else ''
        description = _lang.t(self.description)
        modified = self.f_get('_modified', fmt='pretty_date_time')

        return user, ip, geo, description, modified

    def setup_m_form(self, form, stage: str):
        """Modify form setup hook.
        :type form: pytsite.form.Base
        """
        pass

    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.Ref('user', model='user', nonempty=True))
        self._define_field(_odm.field.String('ip', nonempty=True))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.Virtual('geo_ip'))

        self._define_index(('user', _odm.I_ASC))
        self._define_index(('ip', _odm.I_ASC))

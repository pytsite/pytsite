"""Auth Log ODM Models.
"""
from pytsite import odm as _odm, auth as _auth, geo_ip as _geo_ip

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AuthLog(_odm.Model):
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

    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.Ref('user', model='user', nonempty=True))
        self._define_field(_odm.field.String('ip', nonempty=True))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.Virtual('geo_ip'))

        self._define_index(('user', _odm.I_ASC))
        self._define_index(('ip', _odm.I_ASC))

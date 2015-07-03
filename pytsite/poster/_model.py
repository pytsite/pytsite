"""Poster Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm_ui as _odm_ui, auth as _auth
from pytsite.core import odm as _odm, router as _router, widget as _widget
from . import _functions

class Poster(_odm.Model, _odm_ui.UIMixin):
    """oAuth Account Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('driver', not_empty=True))
        self._define_field(_odm.field.String('source', not_empty=True))
        self._define_field(_odm.field.Ref('account', not_empty=True, model='oauth_account'))
        self._define_field(_odm.field.Ref('owner', model='user', not_empty=True))

        self._define_index([('driver', _odm.I_ASC), ('source', _odm.I_ASC)], True)

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('owner'):
            self.f_set('owner', _auth.get_current_user())

        if self.is_new:
            d = self.f_get('driver')
            s = self.f_get('source')
            if _odm.find('oauth_account').where('driver', '=', d).where('source', '=', s).first():
                raise Exception(self.t('poster_exists', {'name': '{}@{}'.format(d, s)}))

    def setup_browser(self, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = ('driver', 'source', 'owner')

    def get_browser_data_row(self) -> tuple:
        """Hook.
        """
        driver_title = _functions.get_drivers()[self.f_get('driver')][0]
        return driver_title, self.f_get('source'), self.f_get('owner').f_get('full_name')

    def setup_m_form(self, form, stage: str):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        pass

    def submit_m_form(self, form):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        pass

    def get_d_form_description(self) -> str:
        """Hook.
        """
        return self.f_get('driver') + '@' + self.f_get('source')

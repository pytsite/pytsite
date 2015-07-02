"""oAuth Account Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm_ui as _odm_ui
from pytsite.core import odm as _odm

class Account(_odm.Model, _odm_ui.UIMixin):
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('provider', not_empty=True))
        self._define_field(_odm.field.Dict('data', not_empty=True))
        self._define_field(_odm.field.Ref('author', model='user', not_empty=True))

    def setup_browser(self, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = ('provider', 'screen_name', 'owner')

    def get_browser_data_row(self) -> tuple:
        """Hook.
        """
        pass

    def setup_m_form(self, form):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        pass

    def get_d_form_description(self) -> str:
        """Hook.
        """
        pass

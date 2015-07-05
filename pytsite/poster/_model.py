"""Poster Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm_ui as _odm_ui, auth as _auth, content as _content, oauth as _oauth
from pytsite.core import odm as _odm, validation as _validation, lang as _lang
from . import _functions

class Poster(_odm.Model, _odm_ui.UIMixin):
    """oAuth Account Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('content_model', not_empty=True))
        self._define_field(_odm.field.Ref('oauth_account', not_empty=True, model='oauth_account'))
        self._define_field(_odm.field.Ref('owner', model='user', not_empty=True))

        self._define_index([('content_model', _odm.I_ASC), ('oauth_account', _odm.I_ASC)], True)

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('owner'):
            self.f_set('owner', _auth.get_current_user())

    def setup_browser(self, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = ('content_model', 'oauth_account', 'owner')

    def get_browser_data_row(self) -> tuple:
        """Hook.
        """
        content_model = _content.get_model(self.f_get('content_model'))
        oauth_account = self.f_get('oauth_account').f_get('fqsn')
        owner = self.f_get('owner').f_get('full_name')
        return _lang.t(content_model[1]), oauth_account, owner

    def setup_m_form(self, form, stage: str):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        form.add_widget(_content.widget.ContentModelSelect(
            weight=10,
            uid='content_model',
            label=self.t('content_model'),
            value=self.f_get('content_model'),
            h_size='col-sm-6'
        ))

        form.add_widget(_oauth.widget.AccountSelect(
            weight=20,
            uid='oauth_account',
            label=self.t('oauth_account'),
            value=self.f_get('oauth_account'),
            h_size='col-sm-6'
        ))

        form.add_rule('content_model', _validation.rule.NotEmpty())
        form.add_rule('oauth_account', _validation.rule.NotEmpty())

    def submit_m_form(self, form):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        pass

    def get_d_form_description(self) -> str:
        """Hook.
        """
        return str(self.id)

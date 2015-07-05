"""oAuth Account Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm_ui as _odm_ui, auth as _auth
from pytsite.core import odm as _odm, router as _router, widget as _widget
from . import _widget as _oauth_widget, _functions


class Account(_odm.Model, _odm_ui.UIMixin):
    """oAuth Account Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('driver', not_empty=True))
        self._define_field(_odm.field.String('screen_name', not_empty=True))
        self._define_field(_odm.field.Virtual('fqsn'))
        self._define_field(_odm.field.Dict('data', not_empty=True))
        self._define_field(_odm.field.Ref('owner', model='user', not_empty=True))

        self._define_index([('driver', _odm.I_ASC), ('screen_name', _odm.I_ASC)], True)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'fqsn':  # Fully Qualified Screen Name
            driver_name = _functions.get_driver(self.f_get('driver'))[0]
            value = '{}@{}'.format(driver_name, self.f_get('screen_name'))

        return super()._on_f_get(field_name, value, **kwargs)

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('owner'):
            self.f_set('owner', _auth.get_current_user())

        if self.is_new:
            d = self.f_get('driver')
            s = self.f_get('screen_name')
            if _odm.find('oauth_account').where('driver', '=', d).where('screen_name', '=', s).first():
                raise Exception(self.t('account_exists', {'name': '{}@{}'.format(d, s)}))

    def setup_browser(self, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = ('driver', 'screen_name', 'owner')

    def get_browser_data_row(self) -> tuple:
        """Hook.
        """
        driver_title = _functions.get_drivers()[self.f_get('driver')][0]
        return driver_title, self.f_get('screen_name'), self.f_get('owner').f_get('full_name')

    def setup_m_form(self, form, stage: str):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        form.add_widget(_widget.input.Hidden(uid='screen_name', name='screen_name'))

        if self.is_new:
            driver_name = _router.request.values_dict.get('driver')
            # 'First page', select provider
            if not driver_name:
                form.method = 'GET'
                form.action = _router.current_url()
                form.remove_widget('__form_location')
                form.remove_widget('__form_redirect')
                form.remove_widget('__model')
                form.remove_widget('__entity_id')
                form.remove_widget('driver')
                form.add_widget(_oauth_widget.ProviderSelect(
                    uid='driver',
                    label=self.t('driver'),
                    h_size='col-sm-6'
                ))
                submit_btn = form.get_widget('actions').get_child('action_submit')
                """:type: pytsite.core.widget._button.Submit"""
                submit_btn.set_value(self.t('next'))
                submit_btn.icon = 'fa fa-angle-double-right'
            # 'Second page', provider's widget
            else:
                form.add_widget(_widget.input.Hidden(uid='driver', name='driver', value=driver_name))
                driver = _functions.load_driver(driver_name)
                form.add_widget(driver.get_widget('data'))
        else:
            driver = _functions.load_driver(self.f_get('driver'), **self.f_get('data'))
            form.add_widget(driver.get_widget('data', **self.f_get('data')))

    def submit_m_form(self, form):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        data = form.values.get('data')
        screen_name = data.get('screen_name')
        if not screen_name:
            raise Exception(self.t('authorization_did_not_complete'))
        self.f_set('screen_name', data['screen_name'])

    def get_d_form_description(self) -> str:
        """Hook.
        """
        return self.f_get('driver') + '@' + self.f_get('screen_name')

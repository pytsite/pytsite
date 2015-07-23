"""Poster Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm_ui as _odm_ui, auth as _auth, content as _content
from pytsite.core import odm as _odm, validation as _validation, router as _router, widget as _widget
from . import _widget as _content_export_widget, _functions


class ContentExport(_odm.Model, _odm_ui.UIMixin):
    """oAuth Account Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('driver', not_empty=True))
        self._define_field(_odm.field.Dict('driver_opts'))
        self._define_field(_odm.field.String('content_model', not_empty=True))
        self._define_field(_odm.field.Ref('owner', model='user', not_empty=True))

    @property
    def driver(self) -> str:
        return self.f_get('driver')

    @property
    def driver_opts(self) -> dict:
        return self.f_get('driver_opts')

    @property
    def content_model(self) -> str:
        return self.f_get('content_model')

    @property
    def owner(self) -> _auth.model.User:
        return self.f_get('owner')

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('owner'):
            self.f_set('owner', _auth.get_current_user())

    def setup_browser(self, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = ('content_model', 'driver', 'driver_opts', 'owner')

    def get_browser_data_row(self) -> tuple:
        """Hook.
        """
        content_model = _content.get_model_title(self.content_model)
        driver = _functions.get_driver_title(self.driver)
        return content_model, driver, self.driver_opts.get('title', ''), self.owner.full_name

    def setup_m_form(self, form, stage: str):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        req_val = _router.request.values_dict

        if (not req_val.get('content_model') or not req_val.get('driver')) and \
                (not self.content_model or not self.driver):
            form.add_widget(_content.widget.ContentModelSelect(
                weight=10,
                uid='content_model',
                label=self.t('content_model'),
                value=self.content_model,
                h_size='col-sm-6'
            ))

            form.add_widget(_content_export_widget.DriverSelect(
                weight=20,
                uid='driver',
                label=self.t('driver'),
                value=self.driver,
                h_size='col-sm-6'
            ))

            form.method = 'GET'
            form.action = _router.current_url()
            form.remove_widget('__form_location')
            form.remove_widget('__form_redirect')
            form.remove_widget('__entity_id')
            submit_btn = form.get_widget('actions').get_child('action_submit')
            """:type: pytsite.core.widget._button.Submit"""
            submit_btn.set_value(self.t('next'))
            submit_btn.icon = 'fa fa-angle-double-right'
        else:
            content_model = req_val.get('content_model') or self.content_model
            driver = req_val.get('driver') or self.driver

            form.add_widget(_widget.input.Hidden(
                uid='content_model',
                value=content_model
            ))

            form.add_widget(_widget.input.Hidden(
                uid='driver',
                value=driver
            ))

            form.add_widget(_functions.load_driver(driver).get_widget('driver_opts', **self.driver_opts))

        form.add_rule('content_model', _validation.rule.NotEmpty())
        form.add_rule('driver', _validation.rule.NotEmpty())

    def submit_m_form(self, form):
        """Hook.
        :type form: pytsite.core.form.Base
        """
        pass

    def get_d_form_description(self) -> str:
        """Hook.
        """
        return str(self.id)

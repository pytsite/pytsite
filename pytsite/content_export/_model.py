"""Poster Model.
"""
from datetime import datetime as _datetime
from pytsite import odm_ui as _odm_ui, auth as _auth, content as _content, odm as _odm, router as _router, \
    widget as _widget, util as _util
from . import _widget as _content_export_widget, _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ContentExport(_odm.Model, _odm_ui.UIMixin):
    """oAuth Account Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('driver', nonempty=True))
        self._define_field(_odm.field.Dict('driver_opts'))
        self._define_field(_odm.field.String('content_model', nonempty=True))
        self._define_field(_odm.field.Bool('process_all_authors', default=True))
        self._define_field(_odm.field.Bool('with_images_only', default=True))
        self._define_field(_odm.field.Ref('owner', model='user', nonempty=True))
        self._define_field(_odm.field.Bool('enabled', default=True))
        self._define_field(_odm.field.Integer('errors'))
        self._define_field(_odm.field.String('last_error'))
        self._define_field(_odm.field.Integer('max_age', default=14))
        self._define_field(_odm.field.DateTime('paused_till'))
        self._define_field(_odm.field.List('add_tags'))

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

    @property
    def process_all_authors(self) -> bool:
        return self.f_get('process_all_authors')

    @property
    def with_images_only(self) -> bool:
        return self.f_get('with_images_only')

    @property
    def enabled(self) -> bool:
        return self.f_get('enabled')

    @property
    def errors(self) -> int:
        return self.f_get('errors')

    @property
    def last_error(self) -> str:
        return self.f_get('last_error')

    @property
    def max_age(self) -> int:
        return self.f_get('max_age')

    @property
    def paused_till(self) -> _datetime:
        return self.f_get('paused_till')

    @property
    def add_tags(self) -> list:
        return self.f_get('add_tags')

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('owner'):
            self.f_set('owner', _auth.get_current_user())

    def setup_browser(self, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = (
            'content_model',
            'driver',
            'driver_opts',
            'process_all_authors',
            'with_images_only',
            'max_age',
            'enabled',
            'errors',
            'paused_till',
            'owner'
        )

    def get_browser_data_row(self) -> tuple:
        """Hook.
        """
        content_model = _content.get_model_title(self.content_model)
        driver = _functions.get_driver_title(self.driver)
        all_authors = '<span class="label label-success">' + self.t('word_yes') + '</span>' \
            if self.process_all_authors else ''
        w_images = '<span class="label label-success">' + self.t('word_yes') + '</span>' \
            if self.with_images_only else ''
        max_age = self.max_age
        enabled = '<span class="label label-success">' + self.t('word_yes') + '</span>' if self.enabled else ''

        if self.errors:
            errors = '<span class="label label-danger" title="{}">{}</span>'\
                .format(_util.escape_html(self.last_error), self.errors)
        else:
            errors = ''

        paused_till = self.f_get('paused_till', fmt='pretty_date_time') if _datetime.now() < self.paused_till else ''

        return content_model, driver, self.driver_opts.get('title', ''), all_authors, w_images, max_age, enabled, \
               errors, paused_till, self.owner.full_name

    def setup_m_form(self, form, stage: str):
        """Hook.
        :type form: pytsite.form.Base
        """
        inp = _router.request.inp
        step = int(inp.get('step', 0))

        form.add_widget(_widget.select.Checkbox(
            weight=10,
            uid='enabled',
            label=self.t('enabled'),
            value=self.enabled if not step else inp.get('enabled'),
            hidden=True if step else False,
        ))

        form.add_widget(_widget.select.Checkbox(
            weight=20,
            uid='process_all_authors',
            label=self.t('process_all_authors'),
            value=self.process_all_authors if not step else  inp.get('process_all_authors'),
            hidden=True if step else False,
        ))

        form.add_widget(_widget.select.Checkbox(
            weight=30,
            uid='with_images_only',
            label=self.t('with_images_only'),
            value=self.with_images_only if not step else inp.get('with_images_only'),
            hidden=True if step else False,
        ))

        form.add_widget(_content.widget.ModelSelect(
            weight=40,
            uid='content_model',
            check_perms=False,
            label=self.t('content_model'),
            value=self.content_model if not step else inp.get('content_model'),
            h_size='col-sm-4',
            required=True,
            hidden=True if step else False,
        ))

        form.add_widget(_content_export_widget.DriverSelect(
            weight=50,
            uid='driver',
            label=self.t('driver'),
            value=self.driver if not step else inp.get('driver'),
            h_size='col-sm-4',
            required=True,
            hidden=True if step else False,
        ))

        form.add_widget(_widget.input.Integer(
            weight=60,
            uid='max_age',
            label=self.t('max_age'),
            value=self.max_age if not step else inp.get('max_age'),
            h_size='col-sm-1',
            hidden=True if step else False,
        ))

        form.add_widget(_widget.input.Tokens(
            weight=60,
            uid='add_tags',
            label=self.t('additional_tags'),
            value=self.add_tags if not step else inp.get('add_tags'),
            hidden=True if step else False,
        ))

        form.add_widget(_widget.select.DateTime(
            weight=80,
            uid='paused_till',
            label=self.t('paused_till'),
            value=self.paused_till if not step else inp.get('paused_till'),
            h_size='col-sm-5 col-md-4 col-lg-3',
            hidden=True if step else False,
        ))

        form.add_widget(_widget.input.Integer(
            weight=90,
            uid='errors',
            label=self.t('errors'),
            value=self.errors if not step else inp.get('errors'),
            h_size='col-sm-1',
            hidden=True if step else False,
        ))

        if not step:
            form.method = 'GET'
            form.action = _router.current_url()
            form.remove_widget('__form_location')
            form.remove_widget('__form_redirect')
            form.remove_widget('__entity_id')
            submit_btn = form.get_widget('actions').get_child('action_submit')
            """:type: pytsite.widget._button.Submit"""
            submit_btn.set_val(self.t('next'))
            submit_btn.icon = 'fa fa-angle-double-right'

            form.add_widget(_widget.input.Hidden(
                uid='step',
                value=1,
            ))
        # Second step
        else:
            driver = inp.get('driver')
            form.add_widget(_functions.load_driver(driver).get_settings_widget('driver_opts', **self.driver_opts))
            form.add_widget(_widget.input.Hidden(
                uid='step',
                value=3,
            ))

    def get_d_form_description(self) -> str:
        """Hook.
        """
        return '{} ({})'.format(self.driver, self.driver_opts['title'])

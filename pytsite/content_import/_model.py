"""PytSite Content Import ODM Model.
"""
from datetime import datetime as _datetime
from frozendict import frozendict as _frozendict
from pytsite import odm as _odm, odm_ui as _odm_ui, auth as _auth, widget as _widget, content as _content, \
    auth_ui as _auth_ui, util as _util, router as _router, form as _form, lang as _lang, validation as _validation
from . import _widget as _content_import_widget, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ContentImport(_odm_ui.UIEntity):
    """PytSite Content Import ODM Model.
    """
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('driver', nonempty=True))
        self.define_field(_odm.field.Dict('driver_opts'))
        self.define_field(_odm.field.String('content_model', nonempty=True))
        self.define_field(_odm.field.Ref('owner', model='user', nonempty=True))
        self.define_field(_odm.field.Ref('content_author', model='user', nonempty=True))
        self.define_field(_odm.field.Ref('content_section', model='section'))
        self.define_field(_odm.field.String('content_status', nonempty=True))
        self.define_field(_odm.field.String('content_language', nonempty=True))
        self.define_field(_odm.field.Bool('with_images_only', default=True))
        self.define_field(_odm.field.Bool('enabled', default=True))
        self.define_field(_odm.field.Integer('errors'))
        self.define_field(_odm.field.String('last_error'))
        self.define_field(_odm.field.DateTime('paused_till'))
        self.define_field(_odm.field.List('add_tags'))

    @property
    def driver(self) -> str:
        return self.f_get('driver')

    @property
    def driver_opts(self) -> _frozendict:
        return self.f_get('driver_opts')

    @property
    def content_model(self) -> str:
        return self.f_get('content_model')

    @property
    def owner(self) -> _auth.model.User:
        return self.f_get('owner')

    @property
    def content_author(self) -> _auth.model.User:
        return self.f_get('content_author')

    @property
    def content_section(self) -> _content.model.Section:
        return self.f_get('content_section')

    @property
    def content_status(self) -> str:
        return self.f_get('content_status')

    @property
    def content_language(self) -> str:
        return self.f_get('content_language')

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
    def paused_till(self) -> _datetime:
        return self.f_get('paused_till')

    @property
    def add_tags(self) -> tuple:
        return self.f_get('add_tags')

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('owner'):
            self.f_set('owner', _auth.get_current_user())

    @classmethod
    def ui_browser_setup(cls, browser):
        """Hook.
        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = (
            'content_model',
            'driver',
            'driver_opts',
            'content_author',
            'with_images_only',
            'enabled',
            'errors',
            'paused_till',
            'owner'
        )

    def ui_browser_get_row(self) -> tuple:
        model = _content.get_model_title(self.content_model)
        driver = _api.get_driver(self.driver).get_description()
        driver_options = str(dict(self.driver_opts))
        content_author = self.content_author.full_name
        w_images = '<span class="label label-success">' + self.t('word_yes') + '</span>' \
            if self.with_images_only else ''
        enabled = '<span class="label label-success">' + self.t('word_yes') + '</span>' if self.enabled else ''
        paused_till = self.f_get('paused_till', fmt='pretty_date_time') if _datetime.now() < self.paused_till else ''
        owner = self.owner.full_name

        if self.errors:
            errors = '<span class="label label-danger" title="{}">{}</span>'\
                .format(_util.escape_html(self.last_error), self.errors)
        else:
            errors = ''

        return model, driver, driver_options, content_author, w_images, enabled, errors, paused_till, owner

    def ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        frm.steps = 2
        frm.reload_on_forward = True

    def ui_m_form_setup_widgets(self, frm: _form.Form):
        """Setup of a modification form.
        """
        frm.add_widget(_widget.select.Checkbox(
            weight=10,
            uid='enabled',
            label=self.t('enabled'),
            value=self.enabled,
            form_steps=(1,)
        ))

        frm.add_widget(_widget.select.Checkbox(
            weight=20,
            uid='with_images_only',
            label=self.t('with_images_only'),
            value=self.with_images_only,
            form_steps=(1,)
        ))

        frm.add_widget(_content.widget.ModelSelect(
            weight=30,
            uid='content_model',
            label=self.t('content_model'),
            value=self.content_model,
            h_size='col-sm-4',
            required=True,
            form_steps=(1,)
        ))

        frm.add_widget(_widget.select.Language(
            weight=40,
            uid='content_language',
            label=self.t('content_language'),
            value=self.content_language or _lang.get_current(),
            h_size='col-sm-4',
            required=True,
            form_steps=(1,)
        ))

        frm.add_widget(_content.widget.SectionSelect(
            weight=50,
            uid='content_section',
            label=self.t('content_section'),
            value=self.content_section,
            h_size='col-sm-4',
            required=True,
            form_steps=(1,)
        ))

        frm.add_widget(_content.widget.StatusSelect(
            weight=60,
            uid='content_status',
            label=self.t('content_status'),
            value='waiting' if self.is_new else self.content_status,
            h_size='col-sm-4',
            required=True,
            form_steps=(1,)
        ))

        frm.add_widget(_auth_ui.widget.UserSelect(
            weight=70,
            uid='content_author',
            label=self.t('content_author'),
            value=self.content_author if not self.is_new else _auth.get_current_user(),
            h_size='col-sm-4',
            required=True,
            form_steps=(1,)
        ))

        frm.add_widget(_content_import_widget.DriverSelect(
            weight=80,
            uid='driver',
            label=self.t('driver'),
            value=self.driver,
            h_size='col-sm-4',
            required=True,
            form_steps=(1,)
        ))

        frm.add_widget(_widget.input.Tokens(
            weight=90,
            uid='add_tags',
            label=self.t('additional_tags'),
            value=self.add_tags,
            form_steps=(1,)
        ))

        frm.add_widget(_widget.select.DateTime(
            weight=100,
            uid='paused_till',
            label=self.t('paused_till'),
            value=self.paused_till,
            h_size='col-sm-5 col-md-4 col-lg-3',
            form_steps=(1,),
            hidden=self.is_new,
        ))

        frm.add_widget(_widget.input.Integer(
            weight=110,
            uid='errors',
            label=self.t('errors'),
            value=self.errors,
            h_size='col-sm-1',
            form_steps=(1,),
            hidden=self.is_new or not self.errors,
        ))

        # Placeholder widget to give ability to save data while form submit
        frm.add_widget(_widget.input.Hidden(
            weight=120,
            uid='driver_opts',
        ))

        # Replace placeholder widget with real widget provided from driver
        if frm.step == 2:
            driver = _api.get_driver(_router.request().inp.get('driver'))
            settings_widget = driver.get_settings_widget(self.driver_opts)
            settings_widget.uid = 'driver_opts'
            settings_widget.form_step = 2
            frm.replace_widget('driver_opts', settings_widget)
            frm.add_rule('driver_opts', _validation.rule.NonEmpty())

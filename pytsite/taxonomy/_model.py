"""Taxonomy Models.
"""
from pytsite import odm_ui as _odm_ui, lang as _lang, validation as _validation, odm as _odm, widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Term(_odm_ui.Model):
    """Taxonomy Term Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.String('title', nonempty=True))
        self._define_field(_odm.field.String('alias', nonempty=True))
        self._define_field(_odm.field.String('language', nonempty=True, default=_lang.get_current_lang()))
        self._define_field(_odm.field.Integer('weight'))
        self._define_field(_odm.field.Integer('order'))

        self._define_index([('alias', _odm.I_ASC), ('language', _odm.I_ASC)], unique=True)
        self._define_index([('language', _odm.I_ASC), ('weight', _odm.I_DESC)])
        self._define_index([('weight', _odm.I_ASC)])
        self._define_index([('order', _odm.I_ASC)])

    @property
    def title(self) -> str:
        return self.f_get('title')

    @property
    def alias(self) -> str:
        return self.f_get('alias')

    @property
    def language(self) -> str:
        return self.f_get('language')

    @property
    def weight(self) -> int:
        return self.f_get('weight')

    @property
    def order(self) -> int:
        return self.f_get('order')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'alias':
            from . import _functions
            value = value.strip()
            if not self.is_new:
                term = _functions.find(self.model).where('alias', '=', value).first()
                if not term or term.id != self.id:
                    value = _functions.sanitize_alias_string(self.model, value)
            else:
                value = _functions.sanitize_alias_string(self.model, value)

        if field_name == 'language':
            if value not in _lang.get_langs():
                raise ValueError("Language '{}' is not supported.".format(value))

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('alias'):
            self.f_set('alias', self.f_get('title'))

    def setup_browser(self, browser):
        """Hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        browser.data_fields = ('title', 'alias', 'weight', 'order')
        browser.default_sort_field = 'order'
        browser.default_sort_order = _odm.I_ASC

        def finder_adjust(finder: _odm.Finder):
            finder.where('language', '=', _lang.get_current_lang())
        browser.finder_adjust = finder_adjust

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return (
            self.f_get('title'),
            self.f_get('alias'),
            self.f_get('weight'),
            self.f_get('order'),
        )

    def setup_m_form(self, form, stage: str):
        """Hook.
        :type form: pytsite.form.Base
        """
        form.add_widget(_widget.input.Text(
            weight=10,
            uid='title',
            label=self.t('title'),
            value=self.f_get('title'),
        ))

        form.add_widget(_widget.input.Text(
            weight=20,
            uid='alias',
            label=self.t('alias'),
            value=self.f_get('alias'),
        ))

        form.add_widget(_widget.input.Integer(
            weight=30,
            uid='weight',
            label=self.t('weight'),
            value=self.f_get('weight'),
            h_size='col-sm-3 col-md-2 col-lg-1'
        ))

        form.add_widget(_widget.input.Integer(
            weight=40,
            uid='order',
            label=self.t('order'),
            value=self.f_get('order'),
            h_size='col-sm-3 col-md-2 col-lg-1',
            allow_minus=True
        ))

        # Language
        if self.is_new:
            lang_title = _lang.t('lang_title_' + _lang.get_current_lang())
        else:
            lang_title = _lang.t('lang_title_' + self.language)
        form.add_widget((_widget.static.Text(
            weight=900,
            label=self.t('language'),
            title=lang_title,
            value=self.language if self.language else _lang.get_current_lang(),
        )))

        form.add_rule('title', _validation.rule.NotEmpty())

    def get_d_form_description(self) -> str:
        """Hook.
        """
        return self.f_get('title')

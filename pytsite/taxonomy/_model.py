"""Taxonomy Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm_ui
from pytsite.core import lang, validation, odm, widget


class Term(odm.model.ODMModel, odm_ui.model.ODMUIMixin):
    """Taxonomy Term Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(odm.field.String('title', not_empty=True))
        self._define_field(odm.field.String('alias', not_empty=True))
        self._define_field(odm.field.String('language', not_empty=True, default=lang.get_current_lang()))
        self._define_field(odm.field.Integer('weight'))
        self._define_field(odm.field.Integer('order'))

        self._define_index([('alias', odm.I_ASC), ('language', odm.I_ASC)], unique=True)
        self._define_index([('language', odm.I_ASC), ('weight', odm.I_DESC)])
        self._define_index([('weight', odm.I_ASC)])
        self._define_index([('order', odm.I_ASC)])

    def _on_f_set(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'alias':
            from ._manager import sanitize_alias_string
            value = sanitize_alias_string(self.model, value)

        return super()._on_f_set(field_name, value, **kwargs)

    def _pre_save(self):
        """Hook.
        """
        if not self.f_get('alias'):
            self.f_set('alias', self.f_get('title'))

    def save(self):
        if self.is_new:
            from . import _manager
            title = self.f_get('title')
            if _manager.find(self.model).where('title', 'regex_i', '^' + title + '$').count():
                return

        return super().save()

    def setup_browser(self, browser):
        """Hook.

        :type browser: pytsite.odm_ui._browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = ('title', 'alias', 'weight', 'order', 'language')

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return (
            self.f_get('title'),
            self.f_get('alias'),
            self.f_get('weight'),
            self.f_get('order'),
            lang.get_lang_title(self.f_get('language')),
        )

    def setup_m_form(self, form):
        """Hook.

        :type form: pytsite.core.form.Base
        :return: None
        """
        form.add_widget(widget.input.Text(
            weight=10,
            uid='title',
            label=self.t('title'),
            value=self.f_get('title'),
        ))

        form.add_widget(widget.input.Text(
            weight=20,
            uid='alias',
            label=self.t('alias'),
            value=self.f_get('alias'),
        ))

        form.add_widget(widget.input.Integer(
            weight=30,
            uid='weight',
            label=self.t('weight'),
            value=self.f_get('weight'),
            h_size='col-sm-3 col-md-2 col-lg-1',
        ))

        form.add_widget(widget.input.Integer(
            weight=40,
            uid='order',
            label=self.t('order'),
            value=self.f_get('order'),
            h_size='col-sm-3 col-md-2 col-lg-1',
        ))

        form.add_widget(widget.select.LanguageSelect(
            weight=50,
            uid='language',
            label=self.t('language'),
            value=self.f_get('language'),
            h_size='col-sm-4 col-md-3 col-lg-2',
        ))

        form.add_rule('title', validation.rule.NotEmpty())

    def get_d_form_description(self) -> str:
        """Hook.
        """
        return self.f_get('title')

    def t(self, msg_id: str) -> str:
        """Translate a string.
        """
        try:
            return lang.t(self.package() + '@' + msg_id)
        except lang.error.TranslationError:
            return lang.t('pytsite.taxonomy@' + msg_id)

    def t_plural(self, msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        try:
            return lang.t_plural(self.package() + '@' + msg_id, num)
        except lang.error.TranslationError:
            return lang.t_plural('pytsite.taxonomy@' + msg_id, num)

"""Taxonomy Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core.lang import t, t_plural, TranslationError
from pytsite.core.validation.rules import NotEmptyRule
from pytsite.core.odm.models import ODMModel
from pytsite.core.odm import I_ASC
from pytsite.core.odm.fields import *
from pytsite.core.widgets.input import TextInputWidget, IntegerInputWidget
from pytsite.odm_ui.models import ODMUIMixin


class AbstractTerm(ODMModel, ODMUIMixin):
    """Taxonomy Term Model.
    """

    def _setup(self):
        self._define_field(StringField('title', not_empty=True))
        self._define_field(StringField('alias', not_empty=True))
        self._define_field(StringField('language', not_empty=True))
        self._define_field(IntegerField('weight'))
        self._define_field(IntegerField('order'))

        self._define_index([('alias', I_ASC), ('language', I_ASC)], unique=True)
        self._define_index([('weight', I_ASC)])
        self._define_index([('order', I_ASC)])

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        browser.data_fields = ('title', 'alias', 'weight', 'order')

    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return (
            self.f_get('title'),
            self.f_get('alias'),
            self.f_get('weight'),
            self.f_get('order'),
        )

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.forms.BaseForm
        :return: None
        """
        form.add_widget(TextInputWidget(
            weight=10,
            uid='title',
            label=self.t('title'),
            value=self.f_get('title'),
        ))

        form.add_widget(TextInputWidget(
            weight=20,
            uid='alias',
            label=self.t('alias'),
            value=self.f_get('alias'),
        ))

        form.add_widget(IntegerInputWidget(
            weight=30,
            uid='weight',
            label=self.t('weight'),
            value=self.f_get('weight'),
            h_size='col-sm-3 col-md-2 col-lg-1',
        ))

        form.add_widget(IntegerInputWidget(
            weight=40,
            uid='order',
            label=self.t('order'),
            value=self.f_get('order'),
            h_size='col-sm-3 col-md-2 col-lg-1',
        ))

        form.add_rule('title', NotEmptyRule())

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('title')

    def t(self, msg_id: str) -> str:
        """Translate a string.
        """
        try:
            return t(self.package() + '@' + msg_id)
        except TranslationError:
            return t('pytsite.taxonomy@' + msg_id)

    def t_plural(self, msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        try:
            return t_plural(self.package() + '@' + msg_id, num)
        except TranslationError:
            return t_plural('pytsite.taxonomy@' + msg_id, num)

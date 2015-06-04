"""Taxonomy Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from abc import abstractmethod
from pytsite.core.odm.models import ODMModel
from pytsite.core.odm import I_ASC
from pytsite.core.odm.fields import *
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

        :type form: pytsite.core.forms.AbstractForm
        :return: None
        """
        pass

    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        return self.f_get('title')

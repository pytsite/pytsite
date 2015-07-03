"""ODM UI Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite.core import odm as _odm


class UIMixin(_ABC):
    """Base ODM UI Model.
    """
    @_abstractmethod
    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        pass

    @_abstractmethod
    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        pass

    def browser_search(self, finder: _odm.Finder, query: str):
        """Adjust ODM browser finder in search operation.
        """
        for k, field in finder.mock.fields.items():
            if field.__class__ == _odm.field.String:
                finder.or_where(k, 'regex_i', query)

    @_abstractmethod
    def setup_m_form(self, form, stage: str):
        """Modify form setup hook.
        :type form: pytsite.core.form.Base
        """
        pass

    def submit_m_form(self, form):
        """Modify form submit hook.
        :type form: pytsite.core.form.Base
        """
        pass

    @_abstractmethod
    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        pass

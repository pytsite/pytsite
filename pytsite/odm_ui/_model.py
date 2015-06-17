"""ODM UI Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod


class ODMUIMixin(ABC):
    """Base ODM UI Model.
    """

    @abstractmethod
    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.ODMUIBrowser
        :return: None
        """
        pass

    @abstractmethod
    def get_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        pass

    @abstractmethod
    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.form.Base
        """
        pass

    def submit_m_form(self, form):
        """Modify form submit hook.

        :type form: pytsite.core.form.Base
        """
        pass

    @abstractmethod
    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        pass

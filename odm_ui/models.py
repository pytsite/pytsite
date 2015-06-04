"""ODM UI Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from pytsite.core.lang import t, t_plural


class ODMUIMixin(ABC):
    """Base ODM UI Model.
    """

    def package(self) -> str:
        """Get instance's package name.
        """
        return '.'.join(self.__class__.__module__.split('.')[:-1])

    @abstractmethod
    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
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

        :type form: pytsite.core.forms.BaseForm
        :return: None
        """
        pass

    @abstractmethod
    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        pass

    def t(self, msg_id: str) -> str:
        """Translate a string.
        """
        return t(self.package() + '@' + msg_id)

    def t_plural(self, msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        return t_plural(self.package() + '@' + msg_id, num)

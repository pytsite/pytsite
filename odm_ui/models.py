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

    @abstractmethod
    def get_permission_group(self) -> tuple:
        """Get permission group name hook.
        """
        pass

    @abstractmethod
    def get_lang_package(self) -> str:
        """Get language package name hook.
        """
        pass

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

        :type form: pytsite.core.forms.AbstractForm
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
        return t(self.get_lang_package() + '@' + msg_id)

    def t_plural(self, msg_id: str, num: int=2) -> str:
        """Translate a string into plural form.
        """
        return t_plural(self.get_lang_package() + '@' + msg_id, num)

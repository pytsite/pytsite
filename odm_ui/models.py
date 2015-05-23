"""ODM UI Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.lang import t


class ODMUIMixin:
    """Base ODM UI Model.
    """

    def get_permission_group(self) -> str:
        """Get permission group name hook.
        """
        raise NotImplementedError()

    def get_lang_package(self) -> str:
        """Get language package name hook.
        """
        raise NotImplementedError()

    def setup_browser(self, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.browser.ODMUIBrowser
        :return: None
        """
        raise NotImplementedError()

    def get_browser_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        raise NotImplementedError()

    def setup_m_form(self, form):
        """Modify form setup hook.

        :type form: pytsite.core.forms.AbstractForm
        """
        pass

    def submit_m_form(self):
        """Modify form submit hook.
        """
        pass

    def t(self, msg_id: str) -> str:
        return t(self.get_lang_package() + '@' + msg_id)

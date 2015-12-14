"""ODM UI Model.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class UIMixin:
    """Base ODM UI Model.
    """
    @classmethod
    def ui_setup_browser(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        :return: None
        """
        pass

    @property
    def ui_browser_data_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return ()

    @staticmethod
    def ui_is_creation_allowed() -> bool:
        return True

    @staticmethod
    def ui_is_modification_allowed() -> bool:
        return True

    @staticmethod
    def ui_is_deletion_allowed() -> bool:
        return True

    @staticmethod
    def ui_browser_search(finder: _odm.Finder, query: str):
        """Adjust ODM browser finder in search operation.
        """
        for k, field in finder.mock.fields.items():
            if field.__class__ == _odm.field.String:
                finder.or_where(k, 'regex_i', query)

    def ui_setup_m_form(self, form, stage: str):
        """Modify form setup hook.

        :type form: pytsite.form.Base
        """
        pass

    def ui_submit_m_form(self, form):
        """Modify form submit hook.

        :type form: pytsite.form.Base
        """
        pass

    @property
    def ui_d_form_description(self) -> str:
        """Get delete form description.
        """
        return ''


class UIModel(_odm.Model, UIMixin):
    @property
    def ui_d_form_description(self) -> str:
        """Get delete form description.
        """
        return str(self.id)

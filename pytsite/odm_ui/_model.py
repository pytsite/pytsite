"""ODM UI Model.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import odm as _odm, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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

    @staticmethod
    def browser_search(self, finder: _odm.Finder, query: str):
        """Adjust ODM browser finder in search operation.
        """
        for k, field in finder.mock.fields.items():
            if field.__class__ == _odm.field.String:
                finder.or_where(k, 'regex_i', query)

    @_abstractmethod
    def setup_m_form(self, form, stage: str):
        """Modify form setup hook.
        :type form: pytsite.form.Base
        """
        pass

    def submit_m_form(self, form):
        """Modify form submit hook.
        :type form: pytsite.form.Base
        """
        pass

    @_abstractmethod
    def get_d_form_description(self) -> str:
        """Get delete form description.
        """
        pass


class Model(_odm.Model, UIMixin):
    @property
    def can_be_modified(self) -> bool:
        from . import _functions
        return _functions.check_permissions('modify', self.model, self.id)

    @property
    def can_be_deleted(self) -> bool:
        from . import _functions
        return _functions.check_permissions('delete', self.model, self.id)

    def get_delete_url(self, redirect_url: str=None, json=False) -> str:
        args = {
            'model': self.model,
            'ids': str(self.id),
        }

        if json:
            args['json'] = 'true'
        else:
            args['__form_redirect'] = redirect_url if redirect_url else _router.current_url()

        return _router.ep_url('pytsite.odm_ui.ep.post_d_form', args)

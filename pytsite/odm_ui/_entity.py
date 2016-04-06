"""PytSite ODM UI Entity.
"""
from typing import Tuple as _Tuple, Dict as _Dict
from pytsite import odm as _odm, router as _router, form as _form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class UIMixin:
    """Base ODM UI Model.
    """
    @classmethod
    def ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.Browser
        """
        pass

    @classmethod
    def ui_model_creation_allowed(cls) -> bool:
        """Are entities of this MODEL can be CREATED via UI.
        """
        return True

    @classmethod
    def ui_model_modification_allowed(cls) -> bool:
        """Are entities of this MODEL can be MODIFIED via UI.
        """
        return True

    @classmethod
    def ui_model_deletion_allowed(cls) -> bool:
        """Are entities of this MODEL can be DELETED via UI.
        """
        return True

    @classmethod
    def ui_model_actions_enabled(cls) -> bool:
        """Should the 'actions' column be visible in the entities browser.
        """
        return True

    def ui_entity_modification_allowed(self) -> bool:
        """Is this ENTITY can be MODIFIED via UI.
        """
        return self.ui_model_modification_allowed()

    def ui_entity_deletion_allowed(self):
        """Is this ENTITY can be DELETED via UI.
        """
        return self.ui_model_deletion_allowed()

    @classmethod
    def ui_browser_search(cls, finder: _odm.Finder, query: str):
        """Adjust ODM browser finder while performing search.
        """
        if finder.mock.has_text_index:
            finder.where_text(query)
        else:
            for name, field in finder.mock.fields.items():
                if isinstance(field, _odm.field.String):
                    finder.or_where(name, 'regex_i', query)

    @classmethod
    def ui_browser_get_mass_action_buttons(cls) -> _Tuple[_Dict]:
        """Get toolbar mass actions buttons data.
        """
        return ()

    def ui_browser_get_row(self) -> _Tuple:
        """Get single UI browser row.
        """
        return ()

    def ui_browser_get_entity_actions(self) -> _Tuple[_Dict]:
        """Get actions buttons data for single data row.
        """
        return ()

    def ui_mass_action_get_entity_description(self) -> str:
        """Get entity description on mass action forms.
        """
        return ''

    def ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        pass

    def ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        pass

    def ui_m_form_submit(self, frm: _form.Form):
        """Hook.
        """
        pass


class UIEntity(_odm.Entity, UIMixin):
    def ui_mass_action_get_entity_description(self) -> str:
        """Get entity description on mass action forms.
        """
        return str(self.id)

    def ui_entity_modification_allowed(self) -> bool:
        """Is this ENTITY can be MODIFIED via UI.
        """
        if not self.ui_model_modification_allowed():
            return False

        from ._api import check_permissions
        return check_permissions('modify', self.model, self.id)

    def ui_entity_deletion_allowed(self):
        """Is this ENTITY can be DELETED via UI.
        """
        if not self.ui_model_deletion_allowed():
            return False

        from ._api import check_permissions
        return check_permissions('delete', self.model, self.id)

    def ui_m_form_get_url(self, args: dict=None):
        """Get modification form URL.
        """
        if not args:
            args = {}

        args.update({'model': self.model, 'id': str(self.id)})

        return _router.ep_url('pytsite.odm_ui.ep.m_form', args)

    def ui_d_form_get_url(self, ajax: bool=False) -> str:
        """Get URL of deletion form.
        """
        if ajax:
            return _router.ep_url('pytsite.odm_ui.ep.d_form_submit', {
                'model': self.model,
                'ids': str(self.id),
                'ajax': 'true'
            })
        else:
            return _router.ep_url('pytsite.odm_ui.ep.d_form', {
                'model': self.model,
                'ids': str(self.id)
            })

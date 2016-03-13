"""PytSite ODM UI Entity.
"""
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
    def ui_is_model_creation_allowed(cls) -> bool:
        """If the model creation is allowed via UI.
        """
        return True

    @classmethod
    def ui_is_model_modification_allowed(cls) -> bool:
        """If the model modification is allowed via UI.
        """
        return True

    @classmethod
    def ui_is_model_deletion_allowed(cls) -> bool:
        """Is the model deletion allowed via UI.
        """
        return True

    @classmethod
    def ui_is_actions_allowed(cls) -> bool:
        """If the 'actions' column should be enabled.
        """
        return True

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
    def ui_browser_get_mass_action_buttons(cls):
        """Get toolbar mass actions buttons data.

        :rtype: tuple[dict]
        """
        return ()

    def ui_browser_get_row(self) -> tuple:
        """Get single UI browser row.
        """
        return ()

    def ui_is_entity_modification_allowed(self) -> bool:
        """Is ENTITY modification allowed.
        """
        return self.ui_is_model_modification_allowed()

    def ui_is_entity_deletion_allowed(self):
        """Is ENTITY deletion allowed.
        """
        return self.ui_is_model_deletion_allowed()

    def ui_browser_get_entity_actions(self):
        """Get actions buttons data for single data row.

        :rtype: tuple[dict]
        """
        return ()

    def ui_mass_action_get_entity_description(self) -> str:
        """Get description for mass action form.
        """
        return ''

    def ui_m_form_setup(self, frm: _form.Form):
        """Modify form setup hook.
        """
        pass

    def ui_m_form_submit(self, frm: _form.Form):
        """Modify form submit hook.
        """
        pass


class UIEntity(_odm.Entity, UIMixin):
    def ui_mass_action_get_entity_description(self) -> str:
        """Get delete form description.
        """
        return str(self.id)

    def ui_is_entity_modification_allowed(self) -> bool:
        """Is ENTITY modification allowed.
        """
        if not self.ui_is_model_modification_allowed():
            return False

        from ._api import check_permissions
        return check_permissions('modify', self.model, self.id)

    def ui_is_entity_deletion_allowed(self):
        """Is ENTITY deletion allowed.
        """
        if not self.ui_is_model_deletion_allowed():
            return False

        from ._api import check_permissions
        return check_permissions('delete', self.model, self.id)

    def ui_m_form_get_url(self, args: dict=None):
        """Get modification form URL.
        """
        if not args:
            args = {}

        args.update({'model': self.model, 'id': str(self.id)})

        return _router.ep_url('pytsite.odm_ui.ep.get_m_form', args)

    def ui_d_form_get_url(self, ajax: bool=False) -> str:
        """Get deletion form URL.
        """
        if ajax:
            return _router.ep_url('pytsite.odm_ui.ep.post_d_form', {
                'model': self.model,
                'ids': str(self.id),
                'ajax': 'true'
            })
        else:
            return _router.ep_url('pytsite.odm_ui.ep.get_d_form', {
                'model': self.model,
                'ids': str(self.id)
            })

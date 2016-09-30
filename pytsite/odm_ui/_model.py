"""PytSite ODM UI Entity.
"""
from typing import Tuple as _Tuple, Dict as _Dict
from pytsite import odm as _odm, odm_auth as _odm_auth, router as _router, form as _form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class UIEntity(_odm_auth.model.AuthorizableEntity):
    """ODM entity with UI related methods.
    """

    @classmethod
    def odm_ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui.Browser
        """
        pass

    @classmethod
    def odm_ui_browser_search(cls, finder: _odm.Finder, query: str):
        """Adjust ODM browser finder while performing search.
        """
        if finder.mock.has_text_index:
            finder.where_text(query)
        else:
            for name, field in finder.mock.fields.items():
                if isinstance(field, _odm.field.String):
                    finder.or_where(name, 'regex_i', query)

    @classmethod
    def odm_ui_browser_mass_action_buttons(cls) -> _Tuple[_Dict]:
        """Get toolbar mass actions buttons data.
        """
        return ()

    def odm_ui_browser_row(self) -> _Tuple:
        """Get single UI browser row.
        """
        return ()

    @classmethod
    def odm_ui_model_actions_enabled(cls) -> bool:
        """Should the 'actions' column be visible in the entities browser.
        """
        return True

    def odm_ui_browser_entity_actions(self) -> _Tuple[_Dict]:
        """Get actions buttons data for single data row.
        """
        return ()

    def odm_ui_mass_action_entity_description(self) -> str:
        """Get entity description on mass action forms.
        """
        if hasattr(self, 'id'):
            return str(self.id)

    def odm_ui_m_form_setup(self, frm: _form.Form):
        """Hook.
        """
        pass

    def odm_ui_m_form_setup_widgets(self, frm: _form.Form):
        """Hook.
        """
        pass

    def odm_ui_m_form_validate(self, frm: _form.Form):
        """Hook.
        """
        pass

    def odm_ui_m_form_submit(self, frm: _form.Form):
        """Hook.
        """
        pass

    def odm_ui_d_form_submit(self):
        """Hook.
        """
        with self as e:
            e.delete()

    def odm_ui_d_form_url(self, ajax: bool = False) -> str:
        if hasattr(self, 'model') and hasattr(self, 'id'):
            if ajax:
                return _router.ep_url('pytsite.odm_ui@d_form_submit', {
                    'model': self.model,
                    'ids': str(self.id),
                    'ajax': 'true'
                })
            else:
                return _router.ep_url('pytsite.odm_ui@d_form', {
                    'model': self.model,
                    'ids': str(self.id)
                })
        else:
            raise NotImplementedError('Not implemented yet.')

    def odm_ui_m_form_url(self, args: dict = None):
        if hasattr(self, 'model') and hasattr(self, 'id'):
            if not args:
                args = {}

            args.update({
                'model': self.model,
                'id': str(self.id),
                '__redirect': 'ENTITY_VIEW',
            })

            return _router.ep_url('pytsite.odm_ui@m_form', args)

        else:
            raise NotImplementedError('Not implemented yet.')

    def odm_ui_view_url(self) -> str:
        return ''

    @property
    def url(self) -> str:
        return self.odm_ui_view_url()

    @property
    def edit_url(self) -> str:
        return self.odm_ui_m_form_url()

    def as_jsonable(self, **kwargs) -> dict:
        r = super().as_jsonable(**kwargs)

        if self.check_permissions('view'):
            r['url'] = self.url

        if self.check_permissions('modify'):
            r['edit_url'] = self.edit_url

        return r

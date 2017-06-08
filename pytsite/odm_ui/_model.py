"""PytSite ODM UI Entity.
"""
from typing import Tuple as _Tuple, Dict as _Dict
from pytsite import odm as _odm, odm_auth as _odm_auth, router as _router, form as _form, widget as _widget

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
    def odm_ui_creation_allowed(cls) -> bool:
        """Should be UI entity creation function be available.
        """
        return True

    @classmethod
    def odm_ui_modification_allowed(cls) -> bool:
        """Should be UI entity modification function be available.
        """
        return True

    @classmethod
    def odm_ui_deletion_allowed(cls) -> bool:
        """Should be UI entity deletion function be available.
        """
        return True

    @classmethod
    def odm_ui_entity_actions_enabled(cls) -> bool:
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
        weight = 0
        for uid, field in self.fields.items():
            if uid.startswith('_') or field is None:
                continue

            weight += 10

            if isinstance(field, _odm.field.Bool):
                frm.add_widget(_widget.select.Checkbox(
                    uid=uid,
                    weight=weight,
                    label=self.t(uid),
                    required=field.required,
                    default=field.default,
                    value=field.get_val(),
                ))
            elif isinstance(field, _odm.field.Integer):
                frm.add_widget(_widget.input.Integer(
                    uid=uid,
                    weight=weight,
                    label=self.t(uid),
                    required=field.required,
                    default=field.default,
                    value=field.get_val(),
                ))
            elif isinstance(field, _odm.field.Decimal):
                frm.add_widget(_widget.input.Decimal(
                    uid=uid,
                    weight=weight,
                    label=self.t(uid),
                    required=field.required,
                    default=field.default,
                    value=field.get_val(),
                ))
            elif isinstance(field, _odm.field.Email):
                frm.add_widget(_widget.input.Email(
                    uid=uid,
                    weight=weight,
                    label=self.t(uid),
                    required=field.required,
                    default=field.default,
                    value=field.get_val(),
                ))
            elif isinstance(field, _odm.field.MultiLineString):
                frm.add_widget(_widget.input.TextArea(
                    uid=uid,
                    weight=weight,
                    label=self.t(uid),
                    required=field.required,
                    default=field.default,
                    value=field.get_val(),
                ))
            elif isinstance(field, _odm.field.String):
                frm.add_widget(_widget.input.Text(
                    uid=uid,
                    weight=weight,
                    label=self.t(uid),
                    required=field.required,
                    default=field.default,
                    value=field.get_val(),
                ))
            elif isinstance(field, _odm.field.Enum):
                frm.add_widget(_widget.select.Select(
                    uid=uid,
                    weight=weight,
                    label=self.t(uid),
                    required=field.required,
                    items=[(x, self.t(x)) for x in field.valid_values],
                    default=field.default,
                    value=field.get_val(),
                ))

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
        """Shortcut.
        """
        return self.odm_ui_view_url()

    @property
    def modify_url(self) -> str:
        """Shortcut.
        """
        return self.odm_ui_m_form_url()

    def as_jsonable(self, **kwargs) -> dict:
        r = super().as_jsonable(**kwargs)

        view_perm = self.odm_auth_check_permission('view')
        modify_perm = self.odm_auth_check_permission('modify')
        delete_perm = self.odm_auth_check_permission('delete')

        r['permissions'] = {
            'view': view_perm,
            'modify': modify_perm,
            'delete': delete_perm,
        }

        if view_perm:
            r['url'] = self.url

        if modify_perm:
            r['modify_url'] = self.modify_url

        return r

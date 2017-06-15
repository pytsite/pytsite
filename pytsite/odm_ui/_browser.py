"""PytSite ODM Entities Browser.
"""
from typing import Callable as _Callable, Union as _Union
from pytsite import auth, router as _router, metatag as _metatag, odm as _odm, lang as _lang, http as _http, \
    html as _html, http_api as _http_api, odm_auth as _odm_auth, odm_ui as _odm_ui, widget as _widget, \
    permissions as _permission
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Browser(_widget.misc.BootstrapTable):
    """ODM Entities Browser.
    """

    def __init__(self, model: str):
        """Init.
        """
        super().__init__('odm-ui-browser-' + model)

        self._model = model
        if not self._model:
            raise RuntimeError('No model has been specified.')

        # Model class and mock instance
        self._model_class = _api.get_model_class(self._model)
        self._mock = _api.dispense_entity(self._model)

        # Need at least one permission to show entities browser to user
        allow = False
        for p in self._mock.odm_auth_permissions():
            if _odm_auth.check_permission(p, self._model):
                allow = True
                break

        # Was at least one permission found?
        if not allow:
            raise _http.error.Forbidden()

        self._data_url = _http_api.url('pytsite.odm_ui@get_rows', {'model': self._model})
        self._current_user = auth.get_current_user()
        self._finder_adjust = self._default_finder_adjust

        # Browser title
        if not _router.request().is_xhr:
            self._title = self._model_class.t('odm_ui_browser_title_' + self._model)
            _metatag.t_set('title', self._title)
            _metatag.t_set('description', '')

            # 'Create' toolbar button
            if self._mock.odm_auth_check_permission('create') and self._mock.odm_ui_creation_allowed():
                create_form_url = _router.rule_url('pytsite.odm_ui@m_form', {
                    'model': self._model,
                    'eid': '0',
                    '__redirect': _router.current_url(),
                })
                title = _lang.t('pytsite.odm_ui@create')
                btn = _html.A(href=create_form_url, css='btn btn-default add-button', title=title)
                btn.append(_html.I(css='fa fa-fw fa-plus'))
                self._toolbar.append(btn)
                self._toolbar.append(_html.Span('&nbsp;'))

            # 'Delete' toolbar button
            if self._mock.odm_auth_check_permission('delete') and self._mock.odm_ui_deletion_allowed():
                delete_form_url = _router.rule_url('pytsite.odm_ui@d_form', {'model': self._model})
                title = _lang.t('pytsite.odm_ui@delete_selected')
                btn = _html.A(href=delete_form_url, css='hidden btn btn-danger mass-action-button', title=title)
                btn.append(_html.I(css='fa fa-fw fa-remove'))
                self._toolbar.append(btn)
                self._toolbar.append(_html.Span('&nbsp;'))

            # Additional toolbar buttons
            for btn_data in self._model_class.odm_ui_browser_mass_action_buttons():
                ep = btn_data.get('ep')
                url = _router.rule_url(ep) if ep else '#'
                css = 'btn btn-{} mass-action-button'.format(btn_data.get('color', 'default'))
                icon = 'fa fa-fw fa-' + btn_data.get('icon', 'question')
                button = _html.A(href=url, css=css, title=btn_data.get('title'))
                if icon:
                    button.append(_html.I(css=icon))
                self.toolbar.append(button)
                self._toolbar.append(_html.Span('&nbsp;'))

        # Call model's class to perform setup tasks
        self._model_class.odm_ui_browser_setup(self)

        # Head columns
        if not self.data_fields:
            raise RuntimeError("No data fields are defined.")

    @property
    def model(self) -> str:
        """Get browser entities model.
        """
        return self._model

    @property
    def finder_adjust(self) -> _Callable:
        return self._finder_adjust

    @finder_adjust.setter
    def finder_adjust(self, func: _Callable):
        self._finder_adjust = func

    def _default_finder_adjust(self, finder: _odm.Finder):
        pass

    def _build_head_row(self, row: _html.Tr):
        # Actions column
        if self._model_class.odm_ui_entity_actions_enabled():
            row.append(_html.Th(_lang.t('pytsite.odm_ui@actions'), data_field='__actions'))

    def get_rows(self, offset: int = 0, limit: int = 0, sort_field: str = None, sort_order: _Union[int, str] = None,
                 search: str = None) -> dict:
        """Get browser rows.
        """
        r = {'total': 0, 'rows': []}

        # Setup finder
        finder = _odm.find(self._model)
        self._finder_adjust(finder)

        # Permission based limitations if current user can work with only its OWN entities
        show_all = False
        for perm_prefix in ('pytsite.odm_auth.modify.', 'pytsite.odm_auth.delete.'):
            perm_name = perm_prefix + self._model
            if _permission.is_permission_defined(perm_name) and self._current_user.has_permission(perm_name):
                show_all = True
                break

        if not show_all:
            if finder.mock.has_field('author'):
                finder.eq('author', self._current_user.uid)
            elif finder.mock.has_field('owner'):
                finder.eq('owner', self._current_user.uid)

        # Search
        if search:
            self._model_class.odm_ui_browser_search(finder, search)

        # Counting total
        r['total'] = finder.count()

        # Sort
        if sort_field and finder.mock.has_field(sort_field):
            if isinstance(sort_order, int):
                sort_order = _odm.I_DESC if sort_order < 0 else _odm.I_ASC
            elif isinstance(sort_order, str):
                sort_order = _odm.I_DESC if sort_order.lower() == 'desc' else _odm.I_ASC
            else:
                sort_order = _odm.I_ASC
            finder.sort([(sort_field, sort_order)])
        elif self._default_sort_field:
            finder.sort([(self._default_sort_field, self._default_sort_order)])

        # Iterate over result and get content for table rows
        cursor = finder.skip(offset).get(limit)
        for entity in cursor:
            row = entity.odm_ui_browser_row()

            if row is None:
                continue

            if not row:
                raise RuntimeError("'ui_browser_get_row()' returned nothing.")
            if len(row) != len(self.data_fields):
                raise RuntimeError("'ui_browser_get_row()' returned invalid number of cells.")

            # Data TDs
            cell = {}
            for f_name, cell_content in zip([f[0] for f in self._data_fields], row):
                cell[f_name] = cell_content

            # Action buttons
            if self._model_class.odm_ui_entity_actions_enabled():
                actions = self._get_entity_action_buttons(entity)
                for btn_data in entity.odm_ui_browser_entity_actions():
                    color = 'btn btn-xs btn-' + btn_data.get('color', 'default')
                    title = btn_data.get('title', '')
                    ep = btn_data.get('ep')
                    url = _router.rule_url(ep, {'ids': str(entity.id)}) if ep else '#'
                    css = btn_data.get('css', '')
                    i = _html.I(css='fa fa-fw fa-' + btn_data.get('icon', 'question'))
                    btn = _html.A(href=url, css=color + css, title=title).append(i)
                    actions.append(btn).append(_html.TagLessElement('&nbsp;'))

                if not len(actions.children):
                    actions.set_attr('css', actions.get_attr('css') + ' empty')

                cell['__actions'] = actions.render()

            r['rows'].append(cell)

        return r

    @staticmethod
    def _get_entity_action_buttons(entity: _odm_ui.model.UIEntity) -> _html.Div:
        """Get action buttons for entity.
        """
        group = _html.Div(css='entity-actions', data_entity_id=str(entity.id))

        if entity.odm_ui_modification_allowed() and \
                (entity.odm_auth_check_permission('modify') or entity.odm_auth_check_permission('modify_own')):
            m_form_url = _router.rule_url('pytsite.odm_ui@m_form', {
                'model': entity.model,
                'eid': str(entity.id),
                '__redirect': _router.rule_url('pytsite.odm_ui@browse', {'model': entity.model}),
            })
            title = _lang.t('pytsite.odm_ui@modify')
            a = _html.A(css='btn btn-xs btn-default', href=m_form_url, title=title)
            a.append(_html.I(css='fa fa-edit'))
            group.append(a)
            group.append(_html.TagLessElement('&nbsp;'))

        if entity.odm_ui_deletion_allowed() and \
                (entity.odm_auth_check_permission('delete') or entity.odm_auth_check_permission('delete_own')):
            d_form_url = _router.rule_url('pytsite.odm_ui@d_form', {
                'model': entity.model,
                'ids': str(entity.id),
                '__redirect': _router.rule_url('pytsite.odm_ui@browse', {'model': entity.model}),
            })
            title = _lang.t('pytsite.odm_ui@delete')
            a = _html.A(css='btn btn-xs btn-danger', href=d_form_url, title=title)
            a.append(_html.I(css='fa fa-remove'))
            group.append(a)
            group.append(_html.TagLessElement('&nbsp;'))

        return group

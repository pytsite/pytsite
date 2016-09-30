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

        # Checking current user's permissions
        if not _odm_auth.check_permissions('create', self._model) and \
                not _odm_auth.check_permissions('modify', self._model) and \
                not _odm_auth.check_permissions('delete', self._model):
            raise _http.error.Forbidden()

        self._data_url = _http_api.url('odm_ui/browser_rows', model=self._model)
        self._current_user = auth.get_current_user()
        self._finder_adjust = self._default_finder_adjust

        # Model class and mock instance
        self._model_class = _api.get_model_class(self._model)
        self._mock = _api.dispense_entity(self._model)

        # Browser title
        self._title = self._model_class.t('odm_ui_browser_title_' + self._model)
        _metatag.t_set('title', self._title)
        _metatag.t_set('description', '')

        # 'Create' toolbar button
        if self._mock.check_permissions('create'):
            create_form_url = _router.ep_url('pytsite.odm_ui@m_form', {
                'model': self._model,
                'id': '0',
                '__redirect': _router.current_url(),
            })
            title = _lang.t('pytsite.odm_ui@create')
            btn = _html.A(href=create_form_url, cls='btn btn-default add-button', title=title)
            btn.append(_html.I(cls='fa fa-fw fa-plus'))
            self._toolbar.append(btn)
            self._toolbar.append(_html.Span('&nbsp;'))

        # 'Delete' toolbar button
        if self._mock.check_permissions('delete'):
            delete_form_url = _router.ep_url('pytsite.odm_ui@d_form', {'model': self._model})
            title = _lang.t('pytsite.odm_ui@delete_selected')
            btn = _html.A(href=delete_form_url, cls='hidden btn btn-danger mass-action-button', title=title)
            btn.append(_html.I(cls='fa fa-fw fa-remove'))
            self._toolbar.append(btn)
            self._toolbar.append(_html.Span('&nbsp;'))

        # Additional toolbar buttons
        for btn_data in self._model_class.odm_ui_browser_mass_action_buttons():
            ep = btn_data.get('ep')
            url = _router.ep_url(ep) if ep else '#'
            cls = 'btn btn-{} mass-action-button'.format(btn_data.get('color', 'default'))
            icon = 'fa fa-fw fa-' + btn_data.get('icon', 'question')
            button = _html.A(href=url, cls=cls, title=btn_data.get('title'))
            if icon:
                button.append(_html.I(cls=icon))
            self.toolbar.append(button)
            self._toolbar.append(_html.Span('&nbsp;'))

        # Additional assets
        self._assets.extend([
            'pytsite.odm_ui@js/browser.js'
        ])

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
        if self._model_class.odm_ui_model_actions_enabled():
            row.append(_html.Th(_lang.t('pytsite.odm_ui@actions'), data_field='__actions'))

    def get_rows(self, offset: int = 0, limit: int = 0, sort_field: str = None, sort_order: _Union[int, str]=None,
                 search: str = None) -> list:
        """Get browser rows.
        """
        r = {'total': 0, 'rows': []}

        # Setup finder
        finder = _odm.find(self._model)
        self._finder_adjust(finder)

        # Permission based limitations if current user can work with only its OWN entities
        show_all = False
        for perm_prefix in ('pytsite.odm_perm.modify.', 'pytsite.odm_perm.delete.'):
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
            if self._model_class.odm_ui_model_actions_enabled():
                actions = self._get_entity_action_buttons(entity)
                for btn_data in entity.odm_ui_browser_entity_actions():
                    color = 'btn btn-xs btn-' + btn_data.get('color', 'default')
                    title = btn_data.get('title', '')
                    ep = btn_data.get('ep')
                    url = _router.ep_url(ep, {'ids': str(entity.id)}) if ep else '#'
                    cls = btn_data.get('cls', '')
                    i = _html.I(cls='fa fa-fw fa-' + btn_data.get('icon', 'question'))
                    btn = _html.A(href=url, cls=color + cls, title=title).append(i)
                    actions.append(btn).append(_html.TagLessElement('&nbsp;'))

                if not len(actions.children):
                    actions.set_attr('cls', actions.get_attr('cls') + ' empty')

                cell['__actions'] = actions.render()

            r['rows'].append(cell)

        return r

    @staticmethod
    def _get_entity_action_buttons(entity: _odm_ui.model.UIEntity) -> _html.Div:
        """Get action buttons for entity.
        """
        group = _html.Div(cls='entity-actions', data_entity_id=str(entity.id))

        if entity.check_permissions('modify'):
            m_form_url = _router.ep_url('pytsite.odm_ui@m_form', {
                'model': entity.model,
                'id': str(entity.id),
                '__redirect': _router.ep_url('pytsite.odm_ui@browse', {'model': entity.model}),
            })
            title = _lang.t('pytsite.odm_ui@modify')
            a = _html.A(cls='btn btn-xs btn-default', href=m_form_url, title=title)
            a.append(_html.I(cls='fa fa-edit'))
            group.append(a)
            group.append(_html.TagLessElement('&nbsp;'))

        if entity.check_permissions('delete'):
            d_form_url = _router.ep_url('pytsite.odm_ui@d_form', {
                'model': entity.model,
                'ids': str(entity.id),
                '__redirect': _router.ep_url('pytsite.odm_ui@browse', {'model': entity.model}),
            })
            title = _lang.t('pytsite.odm_ui@delete')
            a = _html.A(cls='btn btn-xs btn-danger', href=d_form_url, title=title)
            a.append(_html.I(cls='fa fa-remove'))
            group.append(a)
            group.append(_html.TagLessElement('&nbsp;'))

        return group

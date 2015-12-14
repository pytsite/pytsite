"""PytSite ODM Entities Browser.
"""
from typing import Callable as _Callable
from pytsite import auth, router as _router, assetman as _assetman, metatag as _metatag, browser as _client, \
    odm as _odm, lang as _lang, http as _http, html as _html
from . import _api
from ._model import UIMixin, UIModel

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Browser:
    """ODM Entities Browser.
    """
    def __init__(self, model: str):
        """Init.
        """
        self._title = None
        self._model = model
        self._current_user = auth.get_current_user()
        self._data_fields = ()
        self._default_sort_field = '_modified'
        self._default_sort_order = _odm.I_DESC
        self._finder_adjust = self._default_finder_adjust

        # Checking current user's permissions
        if not self._current_user.has_permission('pytsite.odm_ui.browse.' + model) \
                and not self._current_user.has_permission('pytsite.odm_ui.browse_own.' + model):
            raise _http.error.Forbidden()

        # Mock entity
        self._model_class = _odm.get_model_class(self._model)
        """:type : _odm.models.ODMModel|UIMixin"""

        # Check if the mock implements UI interface
        if not issubclass(self._model_class, UIMixin):
            raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(self._model))

        # Browser title
        self._title = self._model_class.t('odm_ui_browser_title_' + model)
        _metatag.t_set('title', self._title)
        _metatag.t_set('description', '')

        # Call model's class hook to perform setup tasks
        self._model_class.ui_setup_browser(self)

        # Head columns
        if not self.data_fields:
            raise Exception("No data fields are defined.")

        _client.include('bootstrap-table')
        _client.include('font-awesome')
        _assetman.add('pytsite.odm_ui@js/browser.js')

    @property
    def title(self) -> str:
        """Get browser title.
        """
        return self._title

    @title.setter
    def title(self, value):
        """Set browser title.
        """
        self._title = value

    @property
    def data_fields(self) -> tuple:
        """Get browser data fields.
        """
        return self._data_fields

    @data_fields.setter
    def data_fields(self, value: tuple):
        """Set browser data fields.
        """
        if not isinstance(value, tuple):
            raise TypeError('Tuple expected.')

        self._data_fields = value

    @property
    def default_sort_field(self) -> str:
        return self._default_sort_field

    @default_sort_field.setter
    def default_sort_field(self, value: str):
        self._default_sort_field = value

    @property
    def default_sort_order(self) -> int:
        return self._default_sort_order

    @default_sort_order.setter
    def default_sort_order(self, value: int):
        self._default_sort_order = value

    @property
    def finder_adjust(self) -> _Callable:
        return self._finder_adjust

    @finder_adjust.setter
    def finder_adjust(self, func: _Callable):
        self._finder_adjust = func

    def _default_finder_adjust(self, finder: _odm.Finder):
        pass

    def get_table_skeleton(self) -> str:
        """Get browser table skeleton.
        """
        data_url = _router.ep_url('pytsite.odm_ui.ep.get_browser_rows', {'model': self._model})

        # Toolbar
        toolbar = _html.Div(uid='odm-ui-browser-toolbar')

        # 'Create' toolbar button
        if self._model_class.ui_is_creation_allowed() and _api.check_permissions('create', self._model):
            create_form_url = _router.ep_url('pytsite.odm_ui.ep.get_m_form', {'model': self._model, 'id': '0'})
            toolbar.append(
                _html.A(href=create_form_url, cls='btn btn-default add-button').append(
                    _html.I(cls='fa fa-plus')
                )
            )
            toolbar.append(_html.Span('&nbsp;'))

        # 'Delete' toolbar button
        if self._model_class.ui_is_deletion_allowed() and _api.check_permissions('delete', self._model):
            delete_form_url = _router.ep_url('pytsite.odm_ui.ep.get_d_form', {'model': self._model})
            toolbar.append(
                _html.A(href=delete_form_url, cls='btn btn-danger mass-delete-button').append(
                    _html.I(cls='fa fa-remove')
                )
            )

        # Table skeleton
        table = _html.Table(
            data_toggle='table',
            data_url=data_url,
            data_toolbar='#odm-ui-browser-toolbar',
            data_show_refresh='true',
            data_search='true',
            data_pagination='true',
            data_side_pagination='server',
            data_page_size='15',
            data_click_to_select='false',
            data_striped='true',
            data_sort_name=self.default_sort_field,
            data_sort_order='asc' if self.default_sort_order == _odm.I_ASC else 'desc',
        )
        t_head = _html.THead()
        t_body = _html.TBody()
        table.append(t_head).append(t_body)

        # Table head row
        t_head_row = _html.Tr()
        t_head.append(t_head_row)

        # Checkbox column
        t_head_row.append(_html.Th(data_field='__state', data_checkbox='true'))

        # Head cells
        for col in self.data_fields:
            if isinstance(col, str):
                data_field = col
                title = self._model_class.t(col)
            elif isinstance(col, tuple) and len(col) == 2:
                data_field = col[0]
                title = self._model_class.t(col[1])
            else:
                raise ValueError('Invalid format of data field definition.')

            th = _html.Th(title, data_field=data_field, data_sortable='true')
            t_head_row.append(th)

        # Actions column
        t_head_row.append(_html.Th(_lang.t('pytsite.odm_ui@actions'), data_field='__actions'))

        return toolbar.render() + table.render()

    def get_rows(self, offset: int=0, limit: int=0, sort_field: str=None, sort_order: str=None,
                 search: str=None) -> list:
        """Get browser rows.
        """
        r = {'total': 0, 'rows': []}

        # Setup finder
        finder = _odm.find(self._model)
        self._finder_adjust(finder)

        # Counting total
        r['total'] = finder.count()

        # Permissions based limitations if current user can browse only OWN entities
        if not self._current_user.has_permission('pytsite.odm_ui.browse.' + self._model):
            if finder.mock.has_field('author'):
                finder.where('author', '=', self._current_user)
            elif finder.mock.has_field('owner'):
                finder.where('owner', '=', self._current_user)

        # Sort
        if sort_field:
            sort_order = _odm.I_DESC if sort_order.lower() == 'desc' else _odm.I_ASC
            finder.sort([(sort_field, sort_order)])
        else:
            finder.sort([(self.default_sort_field, self.default_sort_order)])

        # Search
        if search:
            self._model_class.ui_browser_search(finder, search)

        # Iterate over result and get content for table rows
        cursor = finder.skip(offset).get(limit)
        for entity in cursor:
            row = entity.ui_browser_data_row

            if row is None:
                continue

            if not row:
                raise Exception("'ui_browser_data_row()' returns nothing.")
            if len(row) != len(self.data_fields):
                raise Exception("'ui_browser_data_row()' returns invalid number of cells.")

            # Data TDs
            cell = {}
            for f_name, cell_content in zip(self.data_fields, row):
                cell[f_name] = cell_content

            # Action buttons
            cell['__actions'] = self._get_entity_action_buttons(entity).render()

            r['rows'].append(cell)

        return r

    def _get_entity_action_buttons(self, entity: UIModel) -> _html.Div:
        """Get action buttons for entity.
        """
        group = _html.Div(cls='entity-actions', data_entity_id=str(entity.id))

        if _api.check_permissions('modify', entity.model, entity.id) and entity.ui_is_modification_allowed():
            href = _router.ep_url('pytsite.odm_ui.ep.get_m_form', {'model': entity.model, 'id': entity.id})
            group.append(_html.A(cls='btn btn-xs btn-default', href=href).append(_html.I(cls='fa fa-edit')))

        if _api.check_permissions('delete', entity.model, entity.id) and entity.ui_is_deletion_allowed():
            group.append(_html.Span('&nbsp;'))
            href = _router.ep_url('pytsite.odm_ui.ep.get_d_form', {'model': entity.model, 'ids': entity.id})
            group.append(_html.A(cls='btn btn-xs btn-danger', href=href).append(_html.I(cls='fa fa-remove')))

        return group

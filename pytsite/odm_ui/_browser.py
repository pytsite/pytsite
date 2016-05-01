"""PytSite ODM Entities Browser.
"""
from typing import Callable as _Callable, Union as _Union
from pytsite import auth, router as _router, assetman as _assetman, metatag as _metatag, browser as _browser, \
    odm as _odm, lang as _lang, http as _http, html as _html
from . import _api
from ._entity import UIEntity

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
        self._data_fields_titles = ()
        self._default_sort_field = '_modified'
        self._default_sort_order = _odm.I_DESC
        self._finder_adjust = self._default_finder_adjust
        self._toolbar = _html.Div(uid='odm-ui-browser-toolbar')

        # Checking current user's permissions
        if not self._current_user.has_permission('pytsite.odm_ui.browse.' + model) \
                and not self._current_user.has_permission('pytsite.odm_ui.browse_own.' + model):
            raise _http.error.Forbidden()

        # Model class and mock instance
        self._model_class = _api.get_model_class(self._model)
        self._mock = _api.dispense_entity(self._model)

        # Browser title
        self._title = self._model_class.t('odm_ui_browser_title_' + model)
        _metatag.t_set('title', self._title)
        _metatag.t_set('description', '')

        # 'Create' toolbar button
        if self._mock.ui_can_be_created():
            create_form_url = _router.ep_url('pytsite.odm_ui.ep.m_form', {'model': self._model, 'id': '0'})
            title = _lang.t('pytsite.odm_ui@create')
            btn = _html.A(href=create_form_url, cls='btn btn-default add-button', title=title)
            btn.append(_html.I(cls='fa fa-fw fa-plus'))
            self._toolbar.append(btn)
            self._toolbar.append(_html.Span('&nbsp;'))

        # 'Delete' toolbar button
        if self._mock.ui_can_be_deleted():
            delete_form_url = _router.ep_url('pytsite.odm_ui.ep.d_form', {'model': self._model})
            title = _lang.t('pytsite.odm_ui@delete_selected')
            btn = _html.A(href=delete_form_url, cls='btn btn-danger mass-action-button', title=title)
            btn.append(_html.I(cls='fa fa-fw fa-remove'))
            self._toolbar.append(btn)
            self._toolbar.append(_html.Span('&nbsp;'))

        # Additional toolbar buttons
        for btn_data in self._model_class.ui_browser_get_mass_action_buttons():
            ep = btn_data.get('ep')
            url = _router.ep_url(ep) if ep else '#'
            cls = 'btn btn-{} mass-action-button'.format(btn_data.get('color', 'default'))
            icon = 'fa fa-fw fa-' + btn_data.get('icon', 'question')
            button = _html.A(href=url, cls=cls, title=btn_data.get('title'))
            if icon:
                button.append(_html.I(cls=icon))
            self.toolbar.append(button)
            self._toolbar.append(_html.Span('&nbsp;'))

        # Call model's class to perform setup tasks
        self._model_class.ui_browser_setup(self)

        # Head columns
        if not self.data_fields:
            raise Exception("No data fields are defined.")

        _browser.include('bootstrap-table')
        _browser.include('font-awesome')
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
    def model(self) -> str:
        """Get browser entities model.
        """
        return self._model

    @property
    def toolbar(self) -> _html.Div:
        return self._toolbar

    @property
    def data_fields(self) -> tuple:
        """Get browser data fields.
        """
        return self._data_fields

    @data_fields.setter
    def data_fields(self, value: _Union[tuple, list]):
        """Set browser data fields.
        """
        if not isinstance(value, (tuple, list)):
            raise TypeError('Tuple or list expected.')

        fields = []
        titles = []
        for f in value:
            if isinstance(f, str):
                fields.append(f)
                titles.append(self._model_class.t(f))
            elif isinstance(f, tuple) and len(f) == 2:
                fields.append(f[0])
                titles.append(self._model_class.t(f[1]))
            else:
                raise TypeError('Invalid format of data field definition.')

        self._data_fields = tuple(fields)
        self._data_fields_titles = tuple(titles)

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

    def get_table(self) -> str:
        """Get browser table skeleton.
        """
        data_url = _router.ep_url('pytsite.odm_ui.ep.browse_get_rows', {'model': self._model})

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
            data_cookie='true',
            data_cookie_id_table='odm_ui_browser_' + self._model,
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
        for field, title in zip(self._data_fields, self._data_fields_titles):
            th = _html.Th(title, data_field=field, data_sortable='true')
            t_head_row.append(th)

        # Actions column
        if self._model_class.ui_model_actions_enabled():
            t_head_row.append(_html.Th(_lang.t('pytsite.odm_ui@actions'), data_field='__actions'))

        return self._toolbar.render() + table.render()

    def get_rows(self, offset: int=0, limit: int=0, sort_field: str=None, sort_order: str=None,
                 search: str=None) -> list:
        """Get browser rows.
        """
        r = {'total': 0, 'rows': []}

        # Setup finder
        finder = _odm.find(self._model)
        self._finder_adjust(finder)

        # Permissions based limitations if current user can browse only OWN entities
        if not self._current_user.has_permission('pytsite.odm_ui.browse.' + self._model):
            if finder.mock.has_field('author'):
                finder.where('author', '=', self._current_user)
            elif finder.mock.has_field('owner'):
                finder.where('owner', '=', self._current_user)

        # Search
        if search:
            self._model_class.ui_browser_search(finder, search)

        # Counting total
        r['total'] = finder.count()

        # Sort
        if sort_field:
            sort_order = _odm.I_DESC if sort_order.lower() == 'desc' else _odm.I_ASC
            finder.sort([(sort_field, sort_order)])
        else:
            finder.sort([(self.default_sort_field, self.default_sort_order)])

        # Iterate over result and get content for table rows
        cursor = finder.skip(offset).get(limit)
        for entity in cursor:
            row = entity.ui_browser_get_row()

            if row is None:
                continue

            if not row:
                raise Exception("'ui_browser_get_row()' returned nothing.")
            if len(row) != len(self.data_fields):
                raise Exception("'ui_browser_get_row()' returned invalid number of cells.")

            # Data TDs
            cell = {}
            for f_name, cell_content in zip(self.data_fields, row):
                cell[f_name] = cell_content

            # Action buttons
            if self._model_class.ui_model_actions_enabled():
                actions = self._get_entity_action_buttons(entity)
                for btn_data in entity.ui_browser_get_entity_actions():
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
    def _get_entity_action_buttons(entity: UIEntity) -> _html.Div:
        """Get action buttons for entity.
        """
        group = _html.Div(cls='entity-actions', data_entity_id=str(entity.id))

        if entity.ui_can_be_modified():
            title = _lang.t('pytsite.odm_ui@modify')
            a = _html.A(cls='btn btn-xs btn-default', href=entity.ui_m_form_url(), title=title)
            a.append(_html.I(cls='fa fa-edit'))
            group.append(a)
            group.append(_html.TagLessElement('&nbsp;'))

        if entity.ui_can_be_deleted():
            title = _lang.t('pytsite.odm_ui@delete')
            a = _html.A(cls='btn btn-xs btn-danger', href=entity.ui_d_form_url(), title=title)
            a.append(_html.I(cls='fa fa-remove'))
            group.append(a)
            group.append(_html.TagLessElement('&nbsp;'))

        return group

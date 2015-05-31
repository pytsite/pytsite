"""ODM Entities Browser.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router, assetman, metatag
from pytsite.core.odm import odm_manager, I_ASC, I_DESC
from pytsite.core.lang import t, get_current_lang
from pytsite.core.html import Div, Table, THead, Span, TBody, Tr, Th, Td, A, I, Input
from pytsite.core.http.errors import Forbidden
from pytsite.core.odm.models import ODMModel
from pytsite.auth import auth_manager
from .models import ODMUIMixin


class ODMUIBrowser:
    """ODM Entities Browser.
    """

    def __init__(self, model: str):
        """Init.
        """

        self._title = None
        self._model = model
        self._current_user = auth_manager.get_current_user()
        self._head_columns = ()

        # Checking permissions
        if not self._current_user.has_permission('pytsite.odm_ui.browse.{}'.format(model)):
            raise Forbidden()

        self._entity_mock = odm_manager.dispense(self._model)
        """:type : ODMUIMixin"""
        if not isinstance(self._entity_mock, ODMUIMixin):
            raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(self._model))

        self._title = self._entity_mock.t(model + '_odm_browser_title')
        metatag.set_tag('title', self._title)

        self._entity_mock.setup_browser(self)

        # Head columns
        if not self.data_fields:
            raise Exception("No head columns are defined.")

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
        return self._head_columns

    @data_fields.setter
    def data_fields(self, value: tuple):
        """Set browser data fields.
        """
        if not isinstance(value, tuple):
            raise TypeError('Tuple expected.')
        self._head_columns = value

    def get_table_skeleton(self) -> str:
        """Get browser table skeleton.
        """

        lang_pkg = self._entity_mock.get_lang_package()
        data_url = router.endpoint_url('pytsite.odm_ui.eps.get_browser_rows', {'model': self._model})

        # Toolbar
        toolbar = Div(uid='odm-ui-browser-toolbar')
        create_form_url = router.endpoint_url('pytsite.odm_ui.eps.get_m_form', {'model': self._model, 'id': '0'})
        toolbar.append(
            A(href=create_form_url, cls='btn btn-default add-button').append(
                I(cls='fa fa-plus')
            )
        )
        toolbar.append(Span('&nbsp;'))
        delete_form_url = router.endpoint_url('pytsite.odm_ui.eps.get_d_form', {'model': self._model})
        toolbar.append(
            A(href=delete_form_url, cls='btn btn-danger mass-delete-button').append(
                I(cls='fa fa-remove')
            )
        )

        # Table skeleton
        table = Table(
            data_toggle='table',
            data_url=data_url,
            data_toolbar='#odm-ui-browser-toolbar',
            data_show_refresh='true',
            data_search='true',
            data_pagination='true',
            data_side_pagination='server',
            data_page_size='25',
            data_click_to_select='false',
            data_striped='true',
        )
        t_head = THead()
        t_body = TBody()
        table.append(t_head).append(t_body)

        # Table head row
        t_head_row = Tr()
        t_head.append(t_head_row)

        # Checkbox column
        t_head_row.append(Th(data_field='__state', data_checkbox='true'))

        # Head cells
        for col in self.data_fields:
            th = Th(t(lang_pkg + '@' + col), data_field=col, data_sortable='true')
            t_head_row.append(th)

        # Actions column
        t_head_row.append(Th(t('pytsite.odm_ui@actions'), data_field='__actions'))

        assetman.add_css('pytsite.tbootstrap@plugins/bootstrap-table/bootstrap-table.min.css')
        assetman.add_js('pytsite.tbootstrap@plugins/bootstrap-table/bootstrap-table.min.js')
        assetman.add_js('pytsite.odm_ui@js/browser.js')

        current_lang = get_current_lang()
        locale = current_lang + '-' + current_lang.upper()
        if current_lang == 'uk':
            locale = 'uk-UA'
        assetman.add_js('pytsite.tbootstrap@plugins/bootstrap-table/locale/bootstrap-table-{}.min.js'. format(locale))

        return toolbar.render() + table.render()

    def get_rows(self, offset: int=0, limit: int=0, sort_field: str=None, sort_order: str=None) -> list:
        """Get browser rows.
        """

        r = {'total': 0, 'rows': []}

        finder = odm_manager.find(self._model)
        r['total'] = finder.count()

        if sort_field:
            sort_order = I_DESC if sort_order.lower() == 'desc' else I_ASC
            finder.sort([(sort_field, sort_order)])

        cursor = finder.skip(offset).get(limit)
        """:type : list[ODMUIMixin|ODMModel]"""
        for entity in cursor:
            # Getting contend for TDs
            cells = entity.get_browser_data_row()
            if not cells:
                raise Exception("'get_browser_row()' returns nothing.")
            if len(cells) != len(self.data_fields):
                raise Exception("'get_browser_row()' returns invalid number of cells.")

            # Data TDs
            cell = {}
            for f_name, cell_content in zip(self.data_fields, cells):
                cell[f_name] = cell_content

            # Action buttons
            cell['__actions'] = self._get_entity_action_buttons(entity).render()

            r['rows'].append(cell)

        return r

    def _get_entity_action_buttons(self, entity) -> Div:
        """Get action buttons for entity.
        """

        group = Div(cls='entity-actions', data_entity_id=str(entity.id))

        if self._check_entity_permission('modify', entity):
            href = router.endpoint_url('pytsite.odm_ui.eps.get_m_form',
                                       {'model': entity.model, 'id': entity.id})
            group.append(A(cls='btn btn-xs btn-default', href=href).append(I(cls='fa fa-edit')))

        if self._check_entity_permission('delete', entity):
            group.append(Span('&nbsp;'))
            href = router.endpoint_url('pytsite.odm_ui.eps.get_d_form',
                                       {'model': entity.model, 'ids': entity.id})
            group.append(A(cls='btn btn-xs btn-danger', href=href).append(I(cls='fa fa-remove')))

        return group

    def _check_entity_permission(self, permission_type: str, entity: ODMModel) -> bool:
        """Check current user's entity permissions.
        """

        if permission_type == 'create':
            return self._current_user.has_permission('pytsite.odm_ui.create.' + self._model)

        if permission_type in ('browse', 'modify', 'delete'):
            if self._current_user.has_permission('pytsite.odm_ui.' + permission_type + '.' + self._model):
                return True
            elif self._current_user.has_permission('pytsite.odm_ui.' + permission_type + '_own.' + self._model):
                if entity.has_field('author') and entity.f_get('author').id == self._current_user.id:
                    return True

        return False

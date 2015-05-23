"""ODM Entities Browser.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router
from pytsite.core.odm import odm_manager
from pytsite.core.lang import t
from pytsite.core.html import Div, Table, THead, TFoot, TBody, Tr, Th, Td, A, I, Label, Input
from pytsite.core.pager import Pager
from pytsite.core.http.errors import Forbidden
from pytsite.core.odm.models import ODMModel
from pytsite.auth import auth_manager
from .models import ODMUIMixin


class ODMUIBrowser:
    def __init__(self, odm_model: str):
        self._title = None
        self._model = odm_model
        self._current_user = auth_manager.get_current_user()
        self._head_columns = ()

        # Checking permissions
        if not self._current_user.has_permission('pytsite.odm_ui.browse.{}'.format(odm_model)):
            raise Forbidden()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def head_columns(self) -> tuple:
        return self._head_columns

    @head_columns.setter
    def head_columns(self, value: tuple):
        if not isinstance(value, tuple):
            raise TypeError('Tuple expected.')
        self._head_columns = value

    def render(self) -> str:
        mock = odm_manager.dispense(self._model)
        if not isinstance(mock, ODMUIMixin):
            raise TypeError("Model '{}' doesn't extend 'ODMUIMixin'".format(self._model))

        lang_pkg = mock.get_lang_package()

        mock.setup_browser(self)

        # Head columns
        if not self.head_columns:
            raise Exception("No head columns are defined.")

        # Table skeleton
        table = Table(cls='table table-bordered table-hover')
        t_head = THead()
        t_body = TBody()
        t_foot = TFoot()
        table.append(t_head).append(t_body).append(t_foot)

        # Table head row
        t_head_row = Tr()
        t_head.append(t_head_row)

        # Head checkbox column
        t_head_row.append(Th(cls='column-checkboxes').append(Input(type='checkbox', cls='check-all')))

        # Head cells
        for col in self.head_columns:
            t_head_row.append(Th(t(lang_pkg + '@' + col)))

        # Head 'action' cell
        t_head_row.append(Th(t('pytsite.odm_ui@actions'), cls='column-actions'))

        # Table rows
        pager = Pager(odm_manager.find(self._model).count())
        finder = odm_manager.find(self._model).skip(pager.skip)
        cursor = finder.get(pager.limit)
        """:type : list[ODMUIMixin]"""
        for entity in cursor:
            tr = Tr()

            # Getting contend for TDs
            columns = entity.get_browser_row()
            if not columns:
                raise Exception("'get_browser_row()' returns nothing.")
            if len(columns) != len(self.head_columns):
                raise Exception("'get_browser_row()' returns invalid number of columns.")

            # Checkbox TD
            tr.append(Td().append(Input(type='checkbox')))

            # Data TDs
            for columns in columns:
                tr.append(Td(columns))

            # Actions TD
            tr.append(Td(self._get_entity_action_buttons(entity).render()))

            t_body.append(tr)

        return table.render()

    def _get_entity_action_buttons(self, entity) -> Div:
        """Get action buttons for entity.
        """

        group = Div(cls='btn-group')
        if self._check_entity_permission('modify', entity):
            href = router.endpoint_url('pytsite.odm_ui.endpoints.get_modify_form',
                                       {'model': entity.model(), 'id': entity.id()})
            group.append(A(cls='btn btn-sm bg-purple', href=href).append(I(cls='fa fa-edit')))
        if self._check_entity_permission('delete', entity):
            href = router.endpoint_url('pytsite.odm_ui.endpoints.get_delete_form',
                                       {'model': entity.model(), 'ids[]': entity.id()})
            group.append(A(cls='btn btn-sm btn-danger', href=href).append(I(cls='fa fa-remove')))

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
                if entity.has_field('author') and entity.f_get('author').id() == self._current_user.id():
                    return True

        return False

"""Various widgets.
"""
from abc import abstractmethod as _abstractmethod
from typing import Union as _Union
from pytsite import html as _html, browser as _browser, lang as _lang
from . import _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class BootstrapTable(_base.Base):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._data_fields = []
        self._data_fields_titles = []
        self._default_sort_field = kwargs.get('default_sort_fields')
        self._default_sort_order = 1
        self._toolbar = _html.Div(uid='bootstrap-table-toolbar')
        self._data_url = kwargs.get('data_url')

        self._assets.extend(_browser.get_assets('bootstrap'))
        self._assets.extend([
            'pytsite.widget@bootstrap-table/bootstrap-table.min.css',
            'pytsite.widget@bootstrap-table/bootstrap-table.min.js',
            'pytsite.widget@bootstrap-table/extensions/cookie/bootstrap-table-cookie.min.js',
            'pytsite.widget@js/bootstrap-table.js',
        ])

        current_lang = _lang.get_current()
        if current_lang != 'en':
            locale = current_lang + '-' + current_lang.upper()
            if current_lang == 'uk':
                locale = 'uk-UA'
            self._assets.append('pytsite.widget@bootstrap-table/locale/bootstrap-table-{}.min.js'.format(locale))

    @property
    def toolbar(self) -> _html.Div:
        return self._toolbar

    @property
    def data_fields(self) -> list:
        """Get browser data fields.
        """
        return self._data_fields

    @data_fields.setter
    def data_fields(self, value: _Union[tuple, list]):
        """Set browser data fields.
        """
        if not isinstance(value, (tuple, list)):
            raise TypeError('Tuple or list expected.')

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

    def _build_head_row(self, row: _html.Tr):
        pass

    @_abstractmethod
    def get_rows(self, offset: int = 0, limit: int = 0, sort_field: str = None, sort_order: str = None,
                 search: str = None) -> list:
        """Get browser rows.
        """
        pass

    def get_html_em(self, **kwargs)-> _html.Element:
        """Get browser table skeleton.
        """
        # Table skeleton
        table = _html.Table(
            data_toggle='table',
            data_url=self._data_url,
            data_toolbar='#bootstrap-table-toolbar',
            data_show_refresh='true',
            data_search='true',
            data_pagination='true',
            data_side_pagination='server',
            data_page_size='10',
            data_click_to_select='false',
            data_striped='true',
            data_sort_name=self._default_sort_field,
            data_sort_order='asc' if self._default_sort_order == 1 else 'desc',
            data_cookie='true',
            data_cookie_id_table='pytsite_widget_misc_bootstrap_table_' + self.uid,
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
        if not isinstance(self._data_fields, (list, tuple)):
            raise TypeError('List or tuple expected.')

        for f in self._data_fields:
            if not isinstance(f, (list, tuple)):
                raise TypeError('List or tuple expected.')
            th = _html.Th(f[1], data_field=f[0], data_sortable='true')
            t_head_row.append(th)

        self._build_head_row(t_head_row)

        r = _html.TagLessElement()
        r.append(self._toolbar)
        r.append(table)

        return r

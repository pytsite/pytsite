"""Static Widgets.
"""
from typing import Union as _Union
from pytsite import html as _html
from . import _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class HTML(_base.Abstract):
    """Wrapper widget for pytsite.html.Element instances.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        :param em: pytsite.html.Element
        """
        super().__init__(uid, **kwargs)

        self._em = kwargs.get('em')
        if not self._em:
            raise ValueError('Element is not specified.')

    def get_html_em(self, **kwargs) -> _html.Element:
        return self._em


class Text(_base.Abstract):
    """Static Text Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._css = ' '.join((self._css, 'widget-static-control'))

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        container = _html.TagLessElement()
        container.append(_html.Input(type='hidden', uid=self.uid, name=self.name, value=self.value))
        container.append(_html.P(self.title, cls='form-control-static'))

        return self._group_wrap(container)


class Table(_base.Abstract):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._thead = []
        self._tbody = []
        self._tfoot = []

    def add_row(self, cells: _Union[list, tuple], index: int = None, part: str = 'tbody'):
        if not isinstance(cells, (list, tuple)):
            raise TypeError('List or tuple expected, got {}'.format(type(cells)))

        if index is None:
            index = len(self._tbody)

        if part == 'thead':
            self._thead.insert(index, cells)
        elif part == 'tfoot':
            self._tfoot.insert(index, cells)
        else:
            self._tbody.insert(index, cells)

    def get_html_em(self, **kwargs) -> _html.Element:
        table = _html.Table(cls='table table-bordered table-hover')

        for part in self._thead, self._tbody, self._tfoot:
            if not part:
                continue

            if part is self._thead:
                t_part = _html.THead()
            elif part is self._tbody:
                t_part = _html.TBody()
            else:
                t_part = _html.TFoot()

            table.append(t_part)

            # Append rows
            for row in part:
                tr = _html.Tr()
                for cell in row:
                    td = _html.Th() if part is self._thead else _html.Td()

                    if isinstance(cell, dict):
                        if 'content' in cell:
                            td.content = cell.pop('content')
                        for attr in cell.keys():
                            td.set_attr(attr, cell[attr])
                    elif isinstance(cell, str):
                        td.content = cell
                    else:
                        raise TypeError('Dict or str expected, got {}'.format(type(cell)))

                    tr.append(td)

                t_part.append(tr)

        return table

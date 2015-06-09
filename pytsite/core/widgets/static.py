"""Static Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import P, Div, Ul, Li, A
from .abstract import AbstractWidget


class HtmlWidget(AbstractWidget):
    """HTML Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._html_em = kwargs.get('html_em', P)

    def render(self) -> str:
        return self._html_em(self._value, cls=self._cls).render()


class StaticControlWidget(HtmlWidget):
    """Static Text Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-static-control'))

    def render(self) -> str:
        """Render the widget.
        """
        return self._group_wrap(self._html_em(self._value, cls='form-control-static'))


class TabsWidget(AbstractWidget):
    """Tabs Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self._tabs = []

    def add_tab(self, tid: str, title: str, content: str):
        """Add a tab.
        """
        tid = tid.replace('.', '-')
        self._tabs.append((tid, title, content))
        return self

    def render(self) -> str:
        wrapper = Div(role='tabpanel')
        tabs_ul = Ul(cls='nav nav-tabs', role='tablist')
        content = Div(cls='tab-content')
        wrapper.append(tabs_ul).append(content)

        i = 0
        for tab in self._tabs:
            tab_uid = 'tab-uid-' + tab[0]
            tabs_ul.append(
                Li(role='presentation', cls='active' if i == 0 else '').append(
                    A(tab[1], href='#' + tab_uid, role='tab', data_toggle='tab')
                )
            )
            content_cls = 'tabpanel tab-pane'
            content_cls += ' active' if i == 0 else ''
            content.append(Div(tab[2], cls=content_cls, uid=tab_uid))
            i += 1

        return self._group_wrap(wrapper.render())

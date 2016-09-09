"""Static Widgets.
"""
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

"""Content Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import tag as _tag
from pytsite.core import widget as _widget, html as _html, lang as _lang
from . import _model, _functions


class ContentModelSelect(_widget.select.Select):
    """Content Model Select Widget.
    """
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self._items = []
        for k, v in _functions.get_models().items():
            self._items.append((k, _lang.t(v[1])))


class TagCloud(_tag.widget.Cloud):
    """Tags Clod Widget.
    """
    def __init__(self, content_model: str, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._link_pattern = '/content/tag/{}/%s'.format(content_model)


class EntityTagCloud(_widget.Base):
    """Tag of the Entity Widget.
    """
    def __init__(self, entity: _model.Content, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._entity = entity
        self._link_pattern = '/content/tag/{}/%s'.format(entity.model)
        self._title_pattern = kwargs.get('title_pattern', '#%s')
        self._term_css = kwargs.get('term_css', 'label label-default')

        self._group_cls += ' widget-content-tags'

    def render(self) -> _html.Element:
        """Render the widget.
        """
        root = _html.Div(child_separator=' ')
        for tag in self._entity.f_get('tags'):
            title = self._title_pattern % tag.f_get('title')
            a_cls = 'tag {}'.format(self._term_css)
            a = _html.A(title, href=self._link_pattern % tag.f_get('alias'), cls=a_cls)
            root.append(a)

        return self._group_wrap(root)

"""Content Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import tag as _tag
from pytsite.core import widget as _widget, html as _html
from . import _model

class TagCloud(_tag.widget.Cloud):
    def __init__(self, content_model: str, **kwargs):
        super().__init__(**kwargs)
        self._link_pattern = '/content/tag/{}/%s'.format(content_model)


class EntityTags(_widget.Base):
    def __init__(self, entity: _model.Content, **kwargs):
        super().__init__(**kwargs)
        self._entity = entity
        self._link_pattern = '/content/tag/{}/%s'.format(entity.model)
        self._title_pattern = kwargs.get('title_pattern', '#%s')
        self._term_css = kwargs.get('term_css', 'label label-default')

        self._group_cls += ' widget-content-tags'

    def render(self) -> _html.Element:
        root = _html.Div(child_separator='&nbsp;')
        for tag in self._entity.f_get('tags'):
            title = self._title_pattern % tag.f_get('title')
            a_cls = 'tag {}'.format(self._term_css)
            a = _html.A(title, href=self._link_pattern % tag.f_get('alias'), cls=a_cls)
            root.append(a)

        return self._group_wrap(root)
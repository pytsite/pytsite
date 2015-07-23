"""Content Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import taxonomy as _taxonomy, auth as _auth
from pytsite.core import widget as _widget, html as _html, lang as _lang
from . import _model, _functions


class ContentModelSelect(_widget.select.Select):
    """Content Model Select Widget.
    """
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self._items = []
        u = _auth.get_current_user()
        for k, v in _functions.get_models().items():
            if u.has_permission('pytsite.odm_ui.browse.' + k) or u.has_permission('pytsite.odm_ui.browse_own.' + k):
                self._items.append((k, _lang.t(v[1])))


class TagCloud(_taxonomy.widget.Cloud):
    """Tags Clod Widget.
    """
    def __init__(self, limit=10, **kwargs):
        """Init.
        """
        super().__init__('tag', limit, **kwargs)


class EntityTagCloud(_widget.Base):
    """Tag of the Entity Widget.
    """
    def __init__(self, entity: _model.Content, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._entity = entity
        self._link_pattern = '/tag/%s'
        self._title_pattern = kwargs.get('title_pattern', '%s')
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

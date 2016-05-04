"""Flag Package Widgets.
"""
from pytsite import auth as _auth, widget as _widget, html as _html, tpl as _tpl, assetman as _assetman
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Flag(_widget.Base):
    """Flag Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        :param entity: pytsite.odm.Model
        :param icon: str
        """
        super().__init__(uid, **kwargs)

        self._entity = kwargs.get('entity')
        if not self._entity:
            raise ValueError('Entity is not specified.')

        _assetman.add('pytsite.flag@css/common.css')

        self._icon = kwargs.get('icon', 'fa fa-star')

    @property
    def entity(self) -> str:
        return self._entity

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def count(self) -> int:
        return _api.count(self._entity)

    def get_html_em(self, **kwargs) -> _html.Element:
        current_user = _auth.get_current_user()

        css = 'widget widget-flag'
        if _api.is_flagged(self._entity, current_user):
            css += ' flagged'

        return _html.Span(_tpl.render('pytsite.flag@widget', {
            'widget': self,
            'current_user': current_user
        }), cls=css, data_entity='{}:{}'.format(self._entity.model, self._entity.id))

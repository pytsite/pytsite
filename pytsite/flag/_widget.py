"""Flag Package Widgets.
"""
from pytsite import auth as _auth, widget as _widget, html as _html, tpl as _tpl, odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Like(_widget.Abstract):
    """Flag Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        :param entity: _odm.model.Entity
        :param icon: str
        """
        super().__init__(uid, **kwargs)

        self._icon = kwargs.get('icon', 'fa fa-fw fa-star')
        self._entity = kwargs.get('entity')
        self._counter = kwargs.get('counter', True)

        if not self._entity:
            raise ValueError('Entity is not specified.')

        self._css += ' widget-flag-like'

        self._assets.extend([
            'pytsite.flag@css/like.css',
            'pytsite.flag@js/like.js',
        ])

        self._data['model'] = self._entity.model
        self._data['uid'] = str(self._entity.id)

    @property
    def entity(self) -> _odm.model.Entity:
        return self._entity

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def count(self) -> int:
        return _api.count(self._entity)

    @property
    def flagged(self) -> int:
        return _api.is_flagged(self._entity, _auth.get_current_user())

    @property
    def counter(self) -> bool:
        return self._counter

    def get_html_em(self, **kwargs) -> _html.Element:
        current_user = _auth.get_current_user()

        if self.flagged:
            self._css += ' flagged'

        return _html.TagLessElement(_tpl.render('pytsite.flag@like', {
            'widget': self,
            'current_user': current_user
        }))

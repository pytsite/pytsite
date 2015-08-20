"""Flag Package Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import auth as _auth
from pytsite.core import widget as _widget, html as _html, tpl as _tpl, odm as _odm, assetman as _assetman


class Flag(_widget.Base):
    """Flag Widget.
    """
    def __init__(self, uid: str, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._uid = uid
        self._icon = kwargs.get('icon', 'fa fa-star')

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def count(self) -> int:
        return _odm.find('flag').where('uid', '=', self._uid).count()

    @property
    def flagged(self) -> bool:
        f = _odm.find('flag').where('uid', '=', self._uid).where('author', '=', _auth.get_current_user())
        return bool(f.count())

    def render(self) -> _html.Element:
        current_user = _auth.get_current_user()

        cls = 'widget flag'
        if not current_user.is_anonymous and self.flagged:
            cls += ' flagged'

        return _html.Span(_tpl.render('pytsite.flag@widget', {
            'widget': self,
            'current_user': current_user
        }), cls=cls, data_uid=self._uid)

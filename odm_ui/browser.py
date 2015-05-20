"""ODM Entities Browser.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.lang import t
from pytsite.core.odm import odm
from pytsite.core.html import Table, THead, TFoot, Th, Tr
from .model import UIModelMixin


class ODMBrowser:
    def __init__(self, model: str):
        self._model = model
        self._entity = odm.dispense(model)
        """:type : UIModelMixin"""

        if not isinstance(self._entity, UIModelMixin):
            raise Exception("ODM model '{}' doesn't extend UIModelMixin.".format(model))

    def render(self) -> str:
        table = Table(class_='table table-bordered table-hover')

        # Table head and foot
        t_head = THead()
        t_foot = TFoot()
        t_head_row = Tr()
        t_foot_row = Tr()
        for th in self._entity.get_browser_columns():
            t_head_row.append(Th(th))
            t_foot_row.append(Th(th))
        t_head_row.append(Th(t('pytsite.core@actions')))
        t_foot_row.append(Th(t('pytsite.core@actions')))
        table.append(t_head.append(t_head_row)).append(t_foot.append(t_foot_row))

        # Table rows


        r = table.render()

        return r

    def _get_entities(self):
        pass

"""ODM UI Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core.lang import t
from pytsite.core.odm.model import ODMModel


class ODMUIModel:
    def get_browser_title(self) -> str:
        pass

    def get_browser_columns_head(self) -> tuple:
        return t('pytsite.odm_ui@id'),

    def get_browser_row(self, entity: ODMModel) -> tuple:
        return str(entity.id()),

    def setup_modify_form(self, entity: ODMModel, form):
        pass

    def submit_modify_form(self):
        pass

"""File Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widgets.abstract import AbstractWidget
from pytsite.core import assetman
from pytsite.core.html import Div


class FilesUploadWidget(AbstractWidget):
    def __init__(self, model: str, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)

        self._model = model

        assetman.add_css('pytsite.file@css/dropzone.min.css')
        assetman.add_js('pytsite.file@js/dropzone.min.js')
        assetman.add_js('pytsite.file@js/widget.js')

    @property
    def model(self) -> str:
        """Get file entities model.
        """

        return self._model

    def render(self) -> str:
        cont = Div(cls='dropzone')
        return self._group_wrap(cont.render(), 'widget-files-upload', {'model': self.model})

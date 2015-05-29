"""File Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widgets.abstract import AbstractWidget
from pytsite.core import assetman, router, tpl
from . import file_manager


class FilesUploadWidget(AbstractWidget):
    """Files Upload Widget.
    """

    def __init__(self, model: str, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)

        # Processing setter filtering
        self.value = self._value

        self._model = model

        self._max_file_size = int(kwargs.get('max_file_size', 2))
        self._max_files = int(kwargs.get('max_files', 0))
        self._accept_files = kwargs.get('accept_files', '*/*')

        assetman.add_css('pytsite.file@css/upload-widget.css')
        assetman.add_js('pytsite.file@js/jquery.iframe-transport.js')
        assetman.add_js('pytsite.file@js/jquery.fileupload.js')
        assetman.add_js('pytsite.file@js/upload-widget.js')

    def render(self) -> str:
        data = {
            'url': router.endpoint_url('pytsite.file.eps.post_upload', {'model': self._model}),
            'model': self._model,
            'max_file_size': self._max_file_size,
            'accept_files': self._accept_files,
        }

        if self._max_files:
            data['max_files'] = self._max_files

        widget_content = tpl.render('pytsite.file@file_upload_widget')

        return self._group_wrap(widget_content, 'widget-files-upload', data)

    def set_value(self, value: list, **kwargs):
        """Set value of the widget.
        """

        if value is None:
            return

        if isinstance(value, str):
            value = [value]

        clean_val = []
        for val in value:
            entity = file_manager.get_by_ref(val)
            if entity:
                clean_val.append(entity)

        if not kwargs.get('validation_mode'):
            to_delete = router.request.get_values_dict().get(self._uid + '_to_delete')
            if to_delete:
                if isinstance(to_delete, str):
                    to_delete = [to_delete]

                for ref in to_delete:
                    file = file_manager.get_by_ref(ref)
                    file.delete()

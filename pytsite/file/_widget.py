"""File Widgets.
"""
from pytsite import widget as _widget, assetman as _assetman, tpl as _tpl, browser as _client, html as _html, \
    router as _router
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class FilesUpload(_widget.Base):
    """Files Upload Widget.
    """
    def __init__(self, model: str, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self._css = ' '.join((self._css, 'widget-files-upload'))

        # Processing setter filtering
        self.set_value(self._value)

        self._model = model
        self._max_file_size = int(kwargs.get('max_file_size', 2))
        self._max_files = int(kwargs.get('max_files', 1))
        self._accept_files = kwargs.get('accept_files', '*/*')
        self._add_btn_label = kwargs.get('add_btn_label', '')
        self._add_btn_icon = kwargs.get('add_btn_icon', 'fa fa-fw fa-plus')
        self._image_max_width = kwargs.get('image_max_width', 0)
        self._image_max_height = kwargs.get('image_max_height', 0)
        self._slot_css = kwargs.get('slot_css', 'col-xs-B-12 col-xs-6 col-md-4 col-lg-3')

        if self._max_files:
            self._data['max_files'] = self._max_files

        _client.include('imagesloaded')
        _assetman.add('pytsite.file@css/upload-widget.css')
        _assetman.add('pytsite.file@js/load-image.all.min.js')
        _assetman.add('pytsite.file@js/canvas-to-blob.min.js')
        _assetman.add('pytsite.file@js/upload-widget.js')

    @property
    def accept_files(self) -> str:
        return self._accept_files

    @accept_files.setter
    def accept_files(self, value: str):
        self._accept_files = value

    @property
    def add_btn_label(self) -> str:
        return self._add_btn_label

    @add_btn_label.setter
    def add_btn_label(self, value: str):
        self._add_btn_label = value

    @property
    def add_btn_icon(self) -> str:
        return self._add_btn_icon

    @add_btn_icon.setter
    def add_btn_icon(self, value: str):
        self._add_btn_icon = value

    @property
    def image_max_width(self) -> int:
        return self._image_max_width

    @image_max_width.setter
    def image_max_width(self, value: int):
        self._image_max_width = value

    @property
    def image_max_height(self) -> int:
        return self._image_max_width

    @image_max_height.setter
    def image_max_height(self, value: int):
        self._image_max_height = value

    @property
    def max_files(self) -> int:
        return self._max_files

    @max_files.setter
    def max_files(self, value: int):
        self._max_files = value

    @property
    def max_file_size(self) -> int:
        return self._max_file_size

    @max_file_size.setter
    def max_file_size(self, value: int):
        self._max_file_size = value

    @property
    def slot_css(self) -> str:
        return self._slot_css

    @slot_css.setter
    def slot_css(self, value: str):
        self._slot_css = value

    def render(self) -> str:
        self._data = {
            'url': _router.ep_url('pytsite.file.eps.upload', {'model': self._model}),
            'model': self._model,
            'max_files': self._max_files if self._max_files else 1,
            'max_file_size': self._max_file_size,
            'accept_files': self._accept_files,
            'image_max_width': self._image_max_width,
            'image_max_height': self._image_max_height,
            'slot_css': self._slot_css
        }

        widget_em = _html.TagLessElement(_tpl.render('pytsite.file@file_upload_widget', {'widget': self}))

        return self._group_wrap(widget_em)

    def set_value(self, value: list, **kwargs):
        """Set value of the widget.
        """
        if value is None:
            return

        if not isinstance(value, list):
            value = [value]

        clean_val = []
        for val in value:
            if not val:
                continue
            entity = _functions.get_by_ref(val)
            if entity:
                clean_val.append(entity)

        # Delete files which are has been removed from the widget.
        to_delete = _router.request.values_dict.get(self._entity + '_to_delete')
        if to_delete and not kwargs.get('validation_mode'):  # IMPORTANT: not in form validation mode
            if isinstance(to_delete, str):
                to_delete = [to_delete]
            for ref in to_delete:
                file = _functions.get_by_ref(ref)
                if file:
                    file.delete()

        self._value = clean_val

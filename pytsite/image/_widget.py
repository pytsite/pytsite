"""Image Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import file as _file


class ImagesUploadWidget(_file.widget.FilesUpload):
    """Images Upload Widget.
    """

    def __init__(self, **kwargs: dict):
        super().__init__(model='image', accept_files='image/*', **kwargs)

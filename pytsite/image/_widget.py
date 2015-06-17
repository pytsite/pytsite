"""Image Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.file._widget import FilesUpload


class ImagesUploadWidget(FilesUpload):
    """Images Upload Widget.
    """

    def __init__(self, **kwargs: dict):
        super().__init__(model='image', accept_files='image/*', **kwargs)

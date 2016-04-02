"""Image Widgets.
"""
from pytsite import file as _file

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ImagesUpload(_file.widget.FilesUpload):
    """Images Upload Widget.
    """
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, model='image', accept_files='image/*', **kwargs)
        self.add_btn_icon = 'fa fa-fw fa-camera'
        self.assets.append('pytsite.image@js/widget-images-upload.js')

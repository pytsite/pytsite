"""Comments Models.
"""
from typing import Tuple as _Tuple
from pytsite import image as _image, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Comment:
    @property
    def thread_id(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def body(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def images(self) -> _Tuple[_image.model.Image]:
        raise NotImplementedError("Not implemented yet")

    @property
    def status(self) -> str:
        raise NotImplementedError("Not implemented yet")

    @property
    def author(self) -> _auth.model.User:
        raise NotImplementedError("Not implemented yet")

"""File Model.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AbstractFile(_ABC):
    @property
    def uid(self) -> str:
        """Get UID of the file.
        """
        return self.get_field('uid')

    @uid.setter
    def uid(self, value: str):
        """Set UID of the file.
        """
        raise RuntimeError("'uid' property is read-only.")

    @property
    def length(self) -> int:
        """Get length of the file in bytes.
        """
        return self.get_field('length')

    @length.setter
    def length(self, value: int):
        """Set length of the file in bytes.
        """
        self.set_field('length', value)

    @property
    def path(self) -> str:
        """Get path of the file relative to storage.
        """
        return self.get_field('path')

    @path.setter
    def path(self, value: str):
        """Set path of the file relative to storage.
        """
        self.set_field('path', value)

    @property
    def local_path(self) -> str:
        """Get path of the file accessible via local filesystem.
        """
        return self.get_field('local_path')

    @local_path.setter
    def local_path(self, value: str) -> str:
        self.set_field('local_path', value)

    @property
    def mime(self) -> str:
        """Get MIME of the file.
        """
        return self.get_field('mime')

    @mime.setter
    def mime(self, value: str):
        """Set MIME of the file.
        """
        self.set_field('mime', value)

    def get_url(self, **kwargs) -> str:
        """Get URL of the file.
        """
        return self.get_field('url', **kwargs)

    @property
    def url(self) -> str:
        """Shortcut.
        """
        return self.get_url()

    def get_thumb_url(self, **kwargs) -> str:
        """Get URL of thumbnail of the file.
        """
        return self.get_field('thumb_url', **kwargs)

    @property
    def thumb_url(self) -> str:
        """Shortcut.
        """
        return self.get_thumb_url()

    @_abstractmethod
    def get_field(self, field_name: str, **kwargs):
        pass

    @_abstractmethod
    def set_field(self, field_name: str, value, **kwargs):
        pass

    @_abstractmethod
    def save(self):
        pass

    @_abstractmethod
    def delete(self):
        pass

    def as_jsonable(self, **kwargs) -> dict:
        return {
            'uid': self.uid,
            'mime': self.mime,
            'length': self.length,
            'url': self.get_url(),
            'thumb_url': self.get_thumb_url(width=kwargs.get('thumb_width', 450),
                                            height=kwargs.get('thumb_height', 450)),
        }


class AbstractImage(AbstractFile):
    @property
    def width(self) -> int:
        """Get width of the image.
        """
        return self.get_field('width')

    @width.setter
    def width(self, value: int):
        """Set width of the image.
        """
        self.set_field('width', value)

    @property
    def height(self) -> int:
        """Get height of the image.
        """
        return self.get_field('height')

    @height.setter
    def height(self, value: int):
        """Set height of the image.
        """
        self.set_field('height', value)

    @property
    def exif(self) -> dict:
        """Get EXIF data of the image.
        """
        return self.get_field('exif')

    @exif.setter
    def exif(self, value: dict):
        """Set EXIF of the image.
        """
        self.set_field('exif', value)

    def get_html(self, alt: str = '', css: str = '', width: int = 0, height: int = 0, enlarge: bool = True):
        """Get HTML code to embed the image.
        """
        if not enlarge:
            if width and width > self.width:
                width = self.width
            if height and height > self.height:
                height = self.height

        css += ' img-responsive'

        return '<img src="{}" class="{}" alt="{}">'.format(
            self.get_url(width=width, height=height), css.strip(), _util.escape_html(alt)
        )

    def get_responsive_html(self, alt: str = '', css: str = '', aspect_ratio: float = None,
                            enlarge: bool = True) -> str:
        """Get HTML code to embed the image (responsive way).
        """
        alt = _util.escape_html(alt)
        css += ' img-responsive pytsite-img'

        return '<span class="{}" data-url="{}" data-alt="{}" data-aspect-ratio="{}" ' \
               'data-width="{}" data-height="{}" data-enlarge="{}"></span>' \
            .format(css.strip(), self.get_url(), alt, aspect_ratio, self.width, self.height, enlarge)

    def as_jsonable(self, **kwargs) -> dict:
        r = super().as_jsonable(**kwargs)
        r.update({
            'width': self.width,
            'height': self.height,
        })

        return r

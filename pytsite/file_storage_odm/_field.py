"""PytSite ODM File Storage Fields.
"""
from typing import Tuple as _Tuple
from bson import DBRef as _DBRef
from pytsite import odm as _odm, file as _file


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _sanitize_finder_arg(arg):
    if isinstance(arg, _file.model.AbstractFile):
        return arg.uid

    elif isinstance(arg, (list, tuple)):
        clean_arg = []
        for img in arg:
            if isinstance(img, _file.model.AbstractFile):
                clean_arg.append(img.uid)
            else:
                clean_arg.append(img)
        return clean_arg

    else:
        return arg


def _get_file(value) -> _file.model.AbstractFile:
    if isinstance(value, _file.model.AbstractFile):
        pass

    elif isinstance(value, str):
        value = _file.get(value)

    # To directly support HTTP API requests
    elif isinstance(value, dict):
        if 'uid' not in value:
            raise ValueError("Dictionary must contain 'uid' key.")

        value = _file.get(value['uid'])

    # Only to support backward compatibility
    elif isinstance(value, _DBRef):
        if value.collection == 'images':
            value = _file.get('file_image:' + str(value.id))
        else:
            raise ValueError('Cannot determine collection of DB reference: {}.'.format(value))

    elif value is None:
        raise _file.error.FileNotFound("File for '{}' is not found.".format(value))

    else:
        raise TypeError('File object, string UID, dict or None expected, got {}'.format(type(value)))

    return value


class AnyFile(_odm.field.Abstract):
    """ODM field to store reference to an image.
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._allowed_mime_group = '*'
        self._file = None

        super().__init__(name, **kwargs)

    def _on_set(self, value, **kwargs) -> str:
        """Hook. Transforms externally set value to internal value.
        """
        try:
            # Extract first image from a list or tuple
            if isinstance(value, (list, tuple)):
                value = value[0] if value else None

            self._file = _get_file(value)
            if self._allowed_mime_group != '*' and not self._file.mime.startswith(self._allowed_mime_group):
                raise TypeError("File MIME '{}' is not allowed here.".format(self._file.mime))

            return self._file.uid

        except _file.error.FileNotFound:
            return None

    def _on_get(self, internal_value: str, **kwargs) -> _file.model.AbstractFile:
        """Hook. Transforms internal value to external one.
        """
        return self._file

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        return _sanitize_finder_arg(arg)


class AnyFiles(_odm.field.UniqueStringList):
    """ODM field to store reference to a list of images.
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._allowed_mime_group = '*'
        self._files = []

        super().__init__(name, **kwargs)

    def _on_set(self, value, **kwargs) -> str:
        """Hook. Transforms externally set value to internal value.
        """
        if not isinstance(value, (list, tuple)):
            value = [value]

        self._files = []
        clean_value = []
        for file in value:
            try:
                file = _get_file(file)

                if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
                    raise TypeError("File MIME '{}' is not allowed here.".format(file.mime))

                clean_value.append(file.uid)
                self._files.append(file)

            except _file.error.FileNotFound:
                pass

        return clean_value

    def _on_get(self, internal_value: str, **kwargs) -> _Tuple[_file.model.AbstractFile]:
        """Hook. Transforms internal value to external one.
        """
        return tuple(self._files)

    def _on_add(self, internal_value, value_to_add, **kwargs):
        """Hook.
        """
        file = _get_file(value_to_add)

        if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
            raise TypeError("File MIME '{}' is not allowed here.".format(file.mime))

        return super()._on_add(internal_value, file.uid)

    def _on_sub(self, internal_value, value_to_sub, **kwargs):
        file = _get_file(value_to_sub)

        if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
            raise TypeError("File MIME '{}' is not allowed here.".format(file.mime))

        return super()._on_sub(internal_value, file.uid)

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        return _sanitize_finder_arg(arg)


class Image(AnyFile):
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, **kwargs)

        self._allowed_mime_group = 'image'


class Images(AnyFiles):
    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, **kwargs)

        self._allowed_mime_group = 'image'

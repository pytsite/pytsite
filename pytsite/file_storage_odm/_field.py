"""PytSite ODM File Storage Fields.
"""
from typing import Optional as _Optional, List as _List, Tuple as _Tuple
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
        return value

    elif isinstance(value, str):
        return _file.get(value)

    # To directly support HTTP API requests
    elif isinstance(value, dict):
        if 'uid' not in value:
            raise ValueError("Dictionary must contain 'uid' key")

        return _file.get(value['uid'])

    # Backward compatibility
    elif isinstance(value, _DBRef):
        if value.collection == 'images':
            return _file.get('file_image:' + str(value.id))
        else:
            raise ValueError('Cannot determine collection of DB reference: {}'.format(value))

    else:
        raise TypeError('File object, string UID or dict expected, got {}'.format(type(value)))


class AnyFile(_odm.field.Abstract):
    """ODM field to store reference to an file
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._allowed_mime_group = '*'

        super().__init__(name, **kwargs)

    def _on_get(self, value: str, **kwargs) -> _Optional[_file.model.AbstractFile]:
        return _get_file(value) if value else None

    def _on_set(self, value, **kwargs) -> _Optional[str]:
        """Hook
        """
        # Extract first file from a list or tuple
        if isinstance(value, (list, tuple)):
            value = value[0] if value else None

        if not value:
            return None

        # Check file's existence
        file = _get_file(value)

        # Check file's MIME type
        if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
            raise TypeError("File MIME '{}' is not allowed here".format(self._file.mime))

        return file.uid

    def sanitize_finder_arg(self, arg):
        """Hook
        """
        return _sanitize_finder_arg(arg)


class AnyFiles(_odm.field.List):
    """ODM field to store reference to a list of files
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._allowed_mime_group = '*'

        super().__init__(name, allowed_types=(_file.model.AbstractFile, str), **kwargs)

    def _on_get(self, internal_value: _List[str], **kwargs) -> _Tuple[_file.model.AbstractFile, ...]:
        return tuple([_get_file(v) for v in internal_value])

    def _on_set(self, value, **kwargs) -> _List[str]:
        """Hook. Transforms externally set value to internal value.
        """
        if not isinstance(value, (list, tuple)):
            value = [value]

        clean_value = []
        for file in value:
            try:
                # Check file's existence
                file = _get_file(file)
            except _file.error.FileNotFound:
                continue

            # Check file's MIME type
            if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
                raise TypeError("File MIME '{}' is not allowed here.".format(file.mime))

            clean_value.append(file.uid)

        return clean_value

    def _on_add(self, internal_value: _List[str], raw_value_to_add, **kwargs):
        """Hook.
        """
        file = _get_file(raw_value_to_add)

        if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
            raise TypeError("File MIME '{}' is not allowed here.".format(file.mime))

        return super()._on_add(internal_value, file.uid)

    def _on_sub(self, internal_value: _List[str], raw_value_to_sub, **kwargs):
        file = _get_file(raw_value_to_sub)

        if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
            raise TypeError("File MIME '{}' is not allowed here.".format(file.mime))

        return super()._on_sub(internal_value, file.uid)

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        return _sanitize_finder_arg(arg)


class Image(AnyFile):
    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, **kwargs)

        self._allowed_mime_group = 'image'


class Images(AnyFiles):
    def __init__(self, name: str, **kwargs):
        """Init
        """
        super().__init__(name, **kwargs)

        self._allowed_mime_group = 'image'

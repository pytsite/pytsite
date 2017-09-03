"""PytSite ODM File Storage Fields.
"""
from typing import Tuple as _Tuple, Optional as _Optional, List as _List
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
            raise ValueError("Dictionary must contain 'uid' key")

        value = _file.get(value['uid'])

    # Backward compatibility
    elif isinstance(value, _DBRef):
        if value.collection == 'images':
            value = _file.get('file_image:' + str(value.id))
        else:
            raise ValueError('Cannot determine collection of DB reference: {}'.format(value))

    elif value is None:
        raise _file.error.FileNotFound("File for '{}' is not found".format(value))

    else:
        raise TypeError('File object, string UID, dict or None expected, got {}'.format(type(value)))

    return value


class AnyFile(_odm.field.Abstract):
    """ODM field to store reference to an file
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        self._allowed_mime_group = '*'

        super().__init__(name, **kwargs)

    def _on_set_storable(self, value: _Optional[str]) -> _file.model.AbstractFile:
        """Hook
        """
        return _get_file(value) if value is not None else value

    def _on_get_storable(self, value: _Optional[_file.model.AbstractFile]) -> _Optional[str]:
        """Hook
        """
        return value.uid if value is not None else value

    def _on_set(self, value, **kwargs) -> _Optional[_file.model.AbstractFile]:
        """Hook
        """
        try:
            # Extract first file from a list or tuple
            if isinstance(value, (list, tuple)):
                value = value[0] if value else None

            # Check file's existence
            file = _get_file(value)

            # Check file's MIME type
            if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
                raise TypeError("File MIME '{}' is not allowed here".format(self._file.mime))

            return file

        except _file.error.FileNotFound:
            # Ignore missing file
            return None

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

        super().__init__(name, allowed_types=(_file.model.AbstractFile,), **kwargs)

    def _on_set_storable(self, value: _List[str]) -> _List[_file.model.AbstractFile]:
        """Hook. Transforms internal value to external one.
        """
        r = []
        for file_uid in value:
            try:
                r.append(_get_file(file_uid))
            except _file.error.FileNotFound:
                # Ignore missing files
                continue

        return r

    def _on_get_storable(self, value: _List[_file.model.AbstractFile]) -> _List[str]:
        return [f.uid for f in value]

    def _on_set(self, value, **kwargs) -> _List[_file.model.AbstractFile]:
        """Hook. Transforms externally set value to internal value.
        """
        if not isinstance(value, (list, tuple)):
            value = [value]

        clean_value = []
        for file in value:
            try:
                # Check file's existence
                file = _get_file(file)

                # Check file's MIME type
                if self._allowed_mime_group != '*' and not file.mime.startswith(self._allowed_mime_group):
                    raise TypeError("File MIME '{}' is not allowed here.".format(file.mime))

                clean_value.append(file)

            except _file.error.FileNotFound:
                # Ignore missing files
                pass

        return clean_value

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

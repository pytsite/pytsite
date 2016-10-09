"""PytSite File ODM Storage Driver.
"""
import os as _os
import re as _re
import shutil as _shutil
import bson.errors as _bson_errors
from mimetypes import guess_extension as _guess_extension
from pytsite import file as _file, reg as _reg, util as _util, odm as _odm
from . import _model


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _build_store_path(mime: str, propose: str = None) -> str:
    """Build unique path to store file on the filesystem.
    """
    extension = _guess_extension(mime)
    storage_dir = _os.path.join(_reg.get('paths.storage'), 'file', 'other')
    store_path = ''
    rnd_str = _util.random_str

    # Determine extension for the file in the storage
    if mime.startswith('image'):
        storage_dir = _os.path.join(_reg.get('paths.storage'), 'file', 'image')
        if extension == '.jpe':
            extension = '.jpg'

    # Possible (but not final) path
    possible_target_path = _os.path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str()) + extension

    # Check if the proposed path suits the requirements
    if propose:
        m = _re.match('(\w{2})/(\w{2})/(\w{16})(\.\w+)$', propose)
        if m:
            extension = m.group(4)
            possible_target_path = _os.path.join(storage_dir, m.group(1), m.group(2), m.group(3)) + extension

    # Search for path which doesn't exist on the filesystem
    while True:
        if not _os.path.exists(possible_target_path):
            store_path = possible_target_path
            break
        else:
            possible_target_path = _os.path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str()) + extension

    return store_path


class Driver(_file.driver.Abstract):
    def create(self, file_path: str, mime: str, name: str = None, description: str = None, propose_path: str = None,
               **kwargs) -> _file.model.AbstractFile:

        # Generating unique file path in storage
        abs_target_path = _build_store_path(mime, propose_path)

        # Make sure that directory on the filesystem exists
        target_dir = _os.path.dirname(abs_target_path)
        if not _os.path.exists(target_dir):
            _os.makedirs(target_dir, 0o755, True)

        # Copy file to the storage
        _shutil.copy(file_path, abs_target_path)

        # Create ODM entity
        if mime.startswith('image'):
            odm_entity = _odm.dispense('file_image')  # type: _model.ImageFileODMEntity
        else:
            odm_entity = _odm.dispense('file_other')  # type: _model.AnyFileODMEntity

        storage_dir = _reg.get('paths.storage')
        odm_entity.f_set('path', abs_target_path.replace(storage_dir + '/', ''))
        odm_entity.f_set('name', name)
        odm_entity.f_set('description', description)
        odm_entity.f_set('mime', mime)
        odm_entity.f_set('length', _os.path.getsize(file_path))
        odm_entity.save()

        if isinstance(odm_entity, _model.ImageFileODMEntity):
            return _model.ImageFile(odm_entity)
        elif isinstance(odm_entity, _model.AnyFileODMEntity):
            return _model.AnyFile(odm_entity)

    def get(self, uid: str) -> _file.model.AbstractFile:
        """Get file by UID.
        """
        # This driver uses UIDs in form 'model:entity_uid'
        uid_split = uid.split(':')
        if len(uid_split) != 2 or not _odm.is_model_registered(uid_split[0]):
            raise ValueError('Invalid file UID format: {}.'.format(uid))

        # Search fo ODM entity in appropriate collection
        try:
            odm_entity = _odm.find(uid_split[0]).eq('_id', uid_split[1]).first()
        except _bson_errors.InvalidId:
            raise _file.error.FileNotFound('ODM entity is not found for file {}.'.format(uid))

        if not odm_entity:
            raise _file.error.FileNotFound('ODM entity is not found for file {}.'.format(uid))

        # Select corresponding file model
        if isinstance(odm_entity, _model.ImageFileODMEntity):
            return _model.ImageFile(odm_entity)
        elif isinstance(odm_entity, _model.AnyFileODMEntity):
            return _model.AnyFile(odm_entity)
        else:
            raise TypeError('Unknown error.')

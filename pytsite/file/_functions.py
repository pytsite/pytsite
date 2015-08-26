"""File manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
import os as _os
import shutil as _shutil
import magic as _magic
from mimetypes import guess_extension as _guess_extension
from urllib.request import urlopen as _urlopen
from urllib.parse import urlparse as _urlparse
from bson.dbref import DBRef as _DBRef
from pytsite import reg as _reg, util as _util, odm as _odm, validation as _validation
from . import _model


def _build_store_path(mime: str, model: str='file', propose: str=None) -> str:
    """Build unique path to store file on the filesystem.
    """
    storage_dir = _os.path.join(_reg.get('paths.storage'), model)
    store_path = ''
    rnd_str = _util.random_str

    extension = _guess_extension(mime)
    if extension == '.jpe':
        extension = '.jpg'

    possible_target_path = _os.path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str(16)) + extension
    if propose:
        m = _re.match('(\w{2})/(\w{2})/(\w{16})(\.\w+)$', propose)
        if m:
            extension = m.group(4)
            possible_target_path = _os.path.join(storage_dir, m.group(1), m.group(2), m.group(3)) + extension

    while True:
        if not _os.path.exists(possible_target_path):
            store_path = possible_target_path
            break
        else:
            possible_target_path = _os.path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str(16)) + extension

    return store_path


def create(source_path: str, name: str=None, description: str=None, model='file', remove_source=False,
           propose_store_path: str=None) -> _model.File:
    """Create a file from path or URL.
    """
    # Store remote file to the local if URL was specified
    url_validator = _validation.Validator()
    url_validator.add_rule('url', _validation.rule.Url(value=source_path))
    if url_validator.validate():
        # Copying remote file to the temporary local file
        with _urlopen(source_path) as src:
            data = src.read()

        tmp_file_fd, tmp_file_path = _util.mk_tmp_file()
        _os.write(tmp_file_fd, data)
        _os.close(tmp_file_fd)

        if not name:
            name = _urlparse(source_path).path.split('/')[-1]
        if not description:
            description = 'Downloaded from ' + source_path

        remove_source = True
        source_path = tmp_file_path

    mime = _magic.from_file(source_path, True).decode()
    abs_target_path = _build_store_path(mime, model, propose_store_path)

    target_dir = _os.path.dirname(abs_target_path)
    if not _os.path.exists(target_dir):
        _os.makedirs(target_dir, 0o755, True)

    # Copy file to the storage
    _shutil.copy(source_path, abs_target_path)

    if not name:
        name = _os.path.basename(source_path)

    if not description:
        description = 'Created from local file ' + source_path

    if remove_source:
        _os.unlink(source_path)

    # Create File entity
    storage_dir = _reg.get('paths.storage')
    file_entity = _odm.dispense(model)
    if not isinstance(file_entity, _model.File):
        raise Exception('File entity expected.')
    file_entity.f_set('path', abs_target_path.replace(storage_dir + '/', ''))
    file_entity.f_set('name', name)
    file_entity.f_set('description', description)
    file_entity.f_set('mime', mime)
    file_entity.f_set('length', _os.stat(abs_target_path).st_size)

    from pytsite import auth
    user = auth.get_current_user()
    if user and not user.is_anonymous:
        file_entity.f_set('owner', user)

    return file_entity.save()


def get(uid: str=None, rel_path: str=None, model: str='file') -> _model.File:
    """Get file.
    """

    if not uid and not rel_path:
        raise Exception("Not enough arguments.")

    if uid:
        return _odm.find(model).where('_id', '=', uid).first()
    elif rel_path:
        return _odm.find(model).where('path', '=', rel_path).first()


def get_by_ref(ref: _DBRef) -> _model.File:
    """Get file by ref.
    """

    entity = _odm.get_by_ref(ref)
    if not entity:
        return

    if not isinstance(entity, _model.File):
        raise Exception('Entity is not File.')

    return entity

"""File manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import magic
from os import path, makedirs, stat, write, unlink
from mimetypes import guess_extension
from shutil import copyfile
from urllib.request import urlopen
from urllib.parse import urlparse
from bson.dbref import DBRef
from pytsite.core import util, reg
from pytsite.core.odm import odm_manager
from pytsite.core.validation.validator import Validator
from pytsite.core.validation.rules import UrlRule
from pytsite.auth import auth_manager
from .models import File


def _build_store_path(mime: str, model: str='file') -> str:
    """Build unique path to store file on the filesystem.
    """
    storage_dir = path.join(reg.get('paths.storage'), model)
    store_path = ''
    rnd_str = util.random_str

    extension = guess_extension(mime)
    if extension == '.jpe':
        extension = '.jpg'

    while True:
        possible_target_path = path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str()) + extension
        if not path.exists(possible_target_path):
            store_path = possible_target_path
            break

    return store_path


def create(source_path: str, name: str=None, description: str=None, model='file', remove_source=False) -> File:
    """Create a file from path or URL.
    """

    # Store remote file to the local if URL was specified
    url_validator = Validator()
    url_validator.add_rule('url', UrlRule(value=source_path))
    if url_validator.validate():
        # Copying remote file to the temporary local file
        with urlopen(source_path) as src:
            data = src.read()

        tmp_file = util.mk_tmp_file()
        write(int(tmp_file[0]), data)

        if not name:
            name = urlparse(source_path).path.split('/')[-1]
        if not description:
            description = 'Downloaded from ' + source_path

        remove_source = True
        source_path = tmp_file[1]

    mime = magic.from_file(source_path, True).decode()
    abs_target_path = _build_store_path(mime, model)

    target_dir = path.dirname(abs_target_path)
    if not path.exists(target_dir):
        makedirs(target_dir, 0o755, True)

    # Copying file to the storage
    copyfile(source_path, abs_target_path)
    if not name:
        name = path.basename(source_path)
    if not description:
        description = 'Created from local file ' + source_path
    if remove_source:
        unlink(source_path)

    # Create File entity
    storage_dir = reg.get('paths.storage')
    file_entity = odm_manager.dispense(model)
    if not isinstance(file_entity, File):
        raise Exception('File entity expected.')
    file_entity.f_set('path', abs_target_path.replace(storage_dir + '/', ''))
    file_entity.f_set('name', name)
    file_entity.f_set('description', description)
    file_entity.f_set('mime', mime)
    file_entity.f_set('length', stat(abs_target_path).st_size)

    user = auth_manager.get_current_user()
    if not user.is_anonymous():
        file_entity.f_set('author', user)

    return file_entity.save()


def get(uid: str=None, rel_path: str=None, model: str='file') -> File:
    """Get file.
    """

    if not uid and not rel_path:
        raise Exception("Not enough arguments.")

    if uid:
        return odm_manager.find(model).where('_id', '=', uid).first()
    elif rel_path:
        return odm_manager.find(model).where('path', '=', rel_path).first()


def get_by_ref(ref: DBRef) -> File:
    """Get file by ref.
    """

    entity = odm_manager.get_by_ref(ref)
    if not entity:
        return

    if not isinstance(entity, File):
        raise Exception('Entity is not File.')

    return entity
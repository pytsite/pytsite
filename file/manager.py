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
from pytsite.core import util, reg, validation, odm
from .models import File


def get_storage_root(model: str='file') -> str:
    return path.join(reg.get('paths.storage'), model)


def _create_store_path(mime: str, model: str='file')->str:
    storage_dir = get_storage_root(model)
    store_path = ''
    rnd_str = util.random_str
    extension = guess_extension(mime)
    while True:
        possible_target_path = path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str()) + extension
        if not path.exists(possible_target_path):
            store_path = possible_target_path
            break

    return store_path


def create(source_path: str, name: str=None, description: str=None, model='file', remove_source=False)->File:
    """Create a file from path or URL.
    """

    # Store remote file to the local if URL was specified
    url_validator = validation.Validator()
    url_validator.add_rule('url', validation.UrlRule(value=source_path))
    if url_validator.validate():
        # Copying remote file to the temporary local file
        with urlopen(source_path) as src:
            data = src.read()

        tmp_file = util.mk_tmp_file()
        write(tmp_file[0], data)

        if not name:
            name = urlparse(source_path).path.split('/')[-1]
        if not description:
            description = 'Downloaded from ' + source_path

        remove_source = True
        source_path = tmp_file[1]

    mime = magic.from_file(source_path, True).decode()
    abs_target_path = _create_store_path(mime, model)

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
    file_entity = odm.manager.dispense(model)
    if not isinstance(file_entity, File):
        raise Exception('File entity expected.')
    file_entity.f_set('path', abs_target_path.replace(storage_dir + '/', ''))
    file_entity.f_set('name', name)
    file_entity.f_set('description', description)
    file_entity.f_set('mime', mime)
    file_entity.f_set('length', stat(abs_target_path).st_size)

    return file_entity.save()


def get(uid: str=None, rel_path: str=None, model: str='file') -> File:
    """Get file.
    """

    if not uid and not rel_path:
        raise Exception("Not enough arguments.")

    if uid:
        return odm.manager.find(model).where('_id', '=', uid).first()
    elif rel_path:
        return odm.manager.find(model).where('path', '=', rel_path).first()

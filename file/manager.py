"""File manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from .models import File


def _create_store_path(mime: str)->str:
    from os import path
    from mimetypes import guess_extension
    from ..core import utils, registry

    storage_dir = registry.get_val('paths.storage')
    store_path = ''
    rnd_str = utils.random_str
    extension = guess_extension(mime)
    while True:
        possible_target_path = path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str()) + extension
        if not path.exists(possible_target_path):
            store_path = possible_target_path
            break

    return store_path


def create(source_path: str, name: str=None, description: str=None, model: str='file')->File:
    """Create a file from path or URL.
    """
    from os import path, makedirs, stat, write
    import magic
    from ..core import validation, registry
    from ..core.odm import manager

    url_validator = validation.Validator()
    url_validator.add_rule('url', validation.UrlRule(value=source_path))
    if url_validator.validate():
        from urllib.request import urlopen
        from urllib.parse import urlparse
        from ..core.utils import mk_tmp_file

        # Copying remote file to the temporary local file
        with urlopen(source_path) as src:
            data = src.read()

        tmp_file = mk_tmp_file()
        write(tmp_file[0], data)

        if not name:
            name = urlparse(source_path).path.split('/')[-1]
        if not description:
            description = 'Downloaded from ' + source_path

        source_path = tmp_file[1]

    mime = magic.from_file(source_path, True).decode()
    abs_target_path = _create_store_path(mime)

    target_dir = path.dirname(abs_target_path)
    if not path.exists(target_dir):
        makedirs(target_dir, 0o755, True)

    # Copying file to the storage
    from shutil import copyfile
    copyfile(source_path, abs_target_path)
    if not name:
        name = path.basename(source_path)
    if not description:
        description = 'Created from local file ' + source_path

    file_entity = manager.dispense(model)
    if not isinstance(file_entity, File):
        raise Exception('File entity expected.')

    storage_dir = registry.get_val('paths.storage')

    file_entity.f_set('path', abs_target_path.replace(storage_dir + '/', ''))
    file_entity.f_set('name', name)
    file_entity.f_set('description', description)
    file_entity.f_set('mime', mime)
    file_entity.f_set('length', stat(abs_target_path).st_size)

    return file_entity.save()

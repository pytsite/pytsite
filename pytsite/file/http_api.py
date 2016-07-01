"""File Plugin Endpoints.
"""
from os import path, unlink
from pytsite import reg as _reg, util as _util, router as _router, odm as _odm, http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_upload(inp: dict) -> list:
    """Upload file endpoint.
    """
    model = inp.get('model')
    if not model:
        raise RuntimeError('Model is not specified.')

    r = []
    files = _router.request().files
    for field_name, f in files.items():
        # Save temporary file
        tmp_path = path.join(_reg.get('paths.tmp'), _util.random_str())
        f.save(tmp_path)
        f.close()

        # Create file entity from temporary file
        try:
            file_entity = _api.create(tmp_path, f.filename, 'Uploaded via HTTP API', model)
        except _odm.error.ForbidEntityCreate as e:
            raise _http.error.Forbidden(e)

        r.append({
            'fid': file_entity.model + ':' + str(file_entity.id),
            'url': file_entity.url,
            'thumb_url': file_entity.thumb_url,
            'name': file_entity.name,
            'description': file_entity.description,
            'mime': file_entity.mime,
            'length': file_entity.length,
        })
        unlink(tmp_path)

    return r

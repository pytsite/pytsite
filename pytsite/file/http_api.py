"""PytSite File HTTP API Endpoints.
"""
from typing import List as _List
from os import path, unlink
from pytsite import reg as _reg, util as _util, router as _router, odm as _odm, http as _http
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_file(inp: dict) -> _List[str]:
    """Upload file endpoint.
    """
    model = inp.get('model')
    if not model:
        raise RuntimeError('Model is not specified.')

    files = _router.request().files
    if not files:
        raise RuntimeError('No files received.')

    r = []
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
            'uid': str(file_entity.id),
        })

        unlink(tmp_path)

    return r


def get_file(inp: dict) -> dict:
    """Get information about file.
    """
    model = inp.get('model')
    if not model:
        raise RuntimeError('Model is not specified.')

    uid = inp.get('uid')
    if not uid:
        raise RuntimeError('File UID is not specified.')

    try:
        entity = _api.get(uid, model=model)

        if entity.model != model:
            raise _http.error.NotFound('File not found.')

        if not entity.check_perm('view'):
            raise _http.error.Forbidden('Insufficient permissions.')

        return entity.as_jsonable(**inp)

    except _error.EntityNotFound:
        raise _http.error.NotFound('File not found.')

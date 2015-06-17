"""File Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path, unlink
from pytsite.core import router, reg, util
from pytsite.core.http._response import JSONResponse, RedirectResponse
from . import _manager


def post_upload(args: dict, inp: dict) -> JSONResponse:
    r = []
    model = args.get('model')
    files = router.request.files
    for field_name, f in files.items():
        tmp_path = path.join(reg.get('paths.tmp'), util.random_str())
        f.save(tmp_path)
        f.close()
        file_entity = _manager.create(tmp_path, f.filename, 'Uploaded via {}.'.format(__name__), model)

        r.append({
            'fid': file_entity.model + ':' + str(file_entity.id),
            'url': file_entity.f_get('url'),
            'thumb_url': file_entity.f_get('thumb_url'),
        })
        unlink(tmp_path)

    return JSONResponse(r)


def get_download(args: dict, inp: dict) -> JSONResponse:
    return JSONResponse('Not implemented yet', 500)

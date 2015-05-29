"""File Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path
from pytsite.core import router, reg, util
from pytsite.core.http.response import JSONResponse
from . import file_manager


def post_upload(args: dict, inp: dict):
    r = []
    model = args.get('model')
    files = router.request.files
    print(files)
    print(inp)
    for field_name, f in files.items():
        tmp_path = path.join(reg.get('paths.tmp'), util.random_str())
        f.save(tmp_path)
        f.close()
        file_entity = file_manager.create(tmp_path, f.filename, 'Uploaded via {}.'.format(__name__), model)
        r.append(file_entity.model + ':' + str(file_entity.id))

    return JSONResponse(r)

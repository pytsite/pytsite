"""File Plugin Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path, unlink
from pytsite import reg as _reg, util as _util, http as _http, router as _router
from . import _functions


def upload(args: dict, inp: dict) -> _http.response.JSON:
    """Upload file endpoint.
    """
    r = []
    model = args.get('model')
    files = _router.request.files
    for field_name, f in files.items():
        tmp_path = path.join(_reg.get('paths.tmp'), _util.random_str())
        f.save(tmp_path)
        f.close()
        file_entity = _functions.create(tmp_path, f.filename, 'Uploaded via {}.'.format(__name__), model)

        r.append({
            'fid': file_entity.model + ':' + str(file_entity.id),
            'url': file_entity.f_get('url'),
            'thumb_url': file_entity.f_get('thumb_url'),
        })
        unlink(tmp_path)

    # Request was from CKEditor
    if inp.get('CKEditor') and inp.get('CKEditorFuncNum'):
        r = r[0]  # From CKEditor only one file can be
        script = 'window.parent.CKEDITOR.tools.callFunction("{}", "{}", "");'\
            .format(inp.get('CKEditorFuncNum'), r['url'])
        return '<script type="text/javascript">{}</script>'.format(script)  # CKEditor requires such answer format

    return _http.response.JSON(r)


def download(args: dict, inp: dict) -> _http.response.JSON:
    """Download file endpoint.
    """
    return _http.response.JSON('Not implemented yet', 500)

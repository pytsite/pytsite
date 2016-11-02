"""PytSite File HTTP API Endpoints.
"""
from typing import List as _List
from os import unlink as _unlink
from pytsite import util as _util, router as _router, http as _http, auth as _auth
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_upload(**kwargs) -> _List[str]:
    """Upload file endpoint.
    """
    files = _router.request().files
    if not files:
        raise RuntimeError('No files received.')

    # It is important to accept files from authenticated users only.
    # At this moment there is no way to store info about file's owner, but in the future things may be changed.
    if _auth.get_current_user().is_anonymous:
        raise _http.error.Forbidden('Access denied.')

    r = []
    for field_name, f in files.items():
        tmp_file_path = _util.mk_tmp_file()[1]
        f.save(tmp_file_path)

        file = _api.create(tmp_file_path, f.filename, 'Uploaded via HTTP API')
        _unlink(tmp_file_path)

        r.append({
            'uid': str(file.uid),
        })

    # Request was from CKEditor
    if kwargs.get('CKEditor') and kwargs.get('CKEditorFuncNum'):
        script = 'window.parent.CKEDITOR.tools.callFunction("{}", "{}", "");' \
            .format(kwargs.get('CKEditorFuncNum'), _api.get(r[0]['uid']).get_url())

        # CKEditor requires such response format
        r = '<script type="text/javascript">{}</script>'.format(script)

    return r


def get_info(**kwargs) -> dict:
    """Get information about file.
    """
    uid = kwargs.get('uid')
    if not uid:
        raise RuntimeError('File UID is not specified.')

    try:
        return _api.get(uid).as_jsonable(**kwargs)

    except _error.FileNotFound as e:
        raise _http.error.NotFound(e)

"""PytSIte Image HTTP API Endpoints.
"""
from pytsite import http_api as _http_api
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_file(inp: dict) -> tuple:
    """Upload an image.
    """
    inp.update({
        'model': 'image',
    })

    # Delegate file creation to the pytsite.file package
    status, body = _http_api.call_ep('pytsite.file@file', 'post', inp)

    # Request was from CKEditor
    if inp.get('CKEditor') and inp.get('CKEditorFuncNum'):
        b = body[0]  # From CKEditor only one file can be uploaded
        script = 'window.parent.CKEDITOR.tools.callFunction("{}", "{}", "");'\
            .format(inp.get('CKEditorFuncNum'), _api.get(b['uid']).url)

        # CKEditor requires such response format
        return status, '<script type="text/javascript">{}</script>'.format(script)

    return status, body


def get_file(inp: dict) -> tuple:
    """Get information about image.
    """
    inp.update({
        'model': 'image',
    })

    return _http_api.call_ep('pytsite.file@file', 'get', inp)

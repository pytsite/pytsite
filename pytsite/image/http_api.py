"""PytSIte Image HTTP API Endpoints.
"""
from pytsite import http_api as _http_api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def post_upload(inp: dict) -> dict:
    inp.update({
        'model': 'image',
    })

    # Delegate file creation to the pytsite.file package
    status, r = _http_api.call_ep('pytsite.file@upload', 'post', inp)

    # Request was from CKEditor
    if inp.get('CKEditor') and inp.get('CKEditorFuncNum'):
        r = r[0]  # From CKEditor only one file can be uploaded
        script = 'window.parent.CKEDITOR.tools.callFunction("{}", "{}", "");'\
            .format(inp.get('CKEditorFuncNum'), r['url'])
        r = '<script type="text/javascript">{}</script>'.format(script)  # CKEditor requires such answer format

    return {'status': status, 'response': r}

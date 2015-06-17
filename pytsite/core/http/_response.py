__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json
from werkzeug.wrappers import Response as _R


class Response(_R):
    """Basic HTTP response.
    """
    pass


class RedirectResponse(Response):
    """Redirect HTTP response.
    """
    def __init__(self, location: str, status: int=302):
        """Init.
        """
        headers = {'Location': location}
        super().__init__('Redirecting to {0}'.format(location), status=status, headers=headers)


class JSONResponse(Response):
    """JSON HTTP response.
    """
    def __init__(self, content, status: int=200):
        """Init.
        """
        super().__init__(json.dumps(content), content_type='application/json', status=status)
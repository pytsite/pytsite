"""PytSite Response Objects
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


import json
from werkzeug.wrappers import Response as _BaseResponse
from ._headers import Headers as _Headers


class Response(_BaseResponse):
    """Basic HTTP response.
    """
    pass


class Redirect(Response):
    """Redirect HTTP response.
    """

    def __init__(self, location: str, status: int = 302):
        """Init.
        """
        headers = {'Location': location}
        super().__init__('Redirecting to {0}'.format(location), status=status, headers=headers)


class JSON(Response):
    """JSON HTTP response.
    """

    def __init__(self, content, status: int = 200, headers: _Headers = None):
        """Init.
        """
        super().__init__(json.dumps(content), status, headers, content_type='application/json')

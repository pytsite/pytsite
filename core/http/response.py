__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from werkzeug.wrappers import Response as BaseResponse


class Response(BaseResponse):
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
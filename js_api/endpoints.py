"""JS API Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router
from pytsite.core.http.response import JSONResponse
from pytsite.core.http.errors import NotFound


def request(args: dict, inp: dict) -> JSONResponse:
    try:
        router.call_endpoint(args.get('endpoint'))
    except ImportError:
        raise NotFound()

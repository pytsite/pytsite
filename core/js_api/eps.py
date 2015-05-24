"""JS API Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router
from pytsite.core.http.response import JSONResponse
from pytsite.core.http.errors import NotFound
from pytsite.core import logger


def request(args: dict, inp: dict) -> JSONResponse:
    ep = args.get('ep')

    try:
        return JSONResponse(router.call_endpoint(ep, args, inp))

    except NotFound:
        return JSONResponse({'error': "Endpoint '{}' is not found.".format(ep)}, status=404)

    except Exception as e:
        logger.error(str(e))
        return JSONResponse({'error': str(e)}, status=500)

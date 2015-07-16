"""JS API Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router, logger, http

def request(args: dict, inp: dict) -> http.response.JSONResponse:
    ep = args.get('ep')

    try:
        return http.response.JSONResponse(router.call_endpoint(ep, args, inp))
    except http.error.NotFound:
        return http.response.JSONResponse({'error': "Endpoint '{}' is not found.".format(ep)}, status=404)
    except Exception as e:
        logger.error(str(e))
        return http.response.JSONResponse({'error': str(e)}, status=500)

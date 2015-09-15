"""JS API Endpoints.
"""
from pytsite import http, router, logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def request(args: dict, inp: dict) -> http.response.JSON:
    ep = args.get('ep')

    try:
        return http.response.JSON(router.call_ep(ep, args, inp))

    except http.error.NotFound:
        return http.response.JSON({'error': "Endpoint '{}' is not found.".format(ep)}, status=404)

    except Exception as e:
        logger.error(str(e), __name__)
        return http.response.JSON({'error': str(e)}, status=500)

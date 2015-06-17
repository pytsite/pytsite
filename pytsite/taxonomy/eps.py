"""Taxonomy Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.http._response import JSONResponse
from . import _manager


def search_terms(args: dict, inp: dict) -> JSONResponse:
    """Get taxonomy terms.
    """
    model = args.get('model')
    query = args.get('query')
    exclude = inp.get('exclude', [])

    if isinstance(exclude, str):
        exclude = [exclude]

    r = []
    finder = _manager.find(model).where('title', 'regex_i', query).where('title', 'nin', exclude)
    for e in finder.get(5):
        r.append(e.f_get('title'))

    return JSONResponse(r)

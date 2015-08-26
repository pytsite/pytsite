"""Taxonomy Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import http as _http
from . import _functions


def search_terms(args: dict, inp: dict) -> _http.response.JSON:
    """Get taxonomy terms.
    """
    model = args.get('model')
    query = args.get('query')
    exclude = inp.get('exclude', [])

    if isinstance(exclude, str):
        exclude = [exclude]

    r = []
    finder = _functions.find(model).where('title', 'nin', exclude)

    for word in query.split(' '):
        finder.where('title', 'regex_i', word.strip())

    for e in finder.get(10):
        r.append(e.f_get('title'))

    return _http.response.JSON(r)

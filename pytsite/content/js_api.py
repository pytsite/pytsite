"""PytSite Content JS API Endpoints.
"""
from pytsite import lang as _lang, auth as _auth, http as _http, odm as _odm, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def search(inp: dict) -> dict:
    from . import _api

    # Query is mandatory parameter
    query = inp.get('q')
    if not query:
        return {'results': ()}

    # Anonymous users cannot perform search
    user = _auth.current_user()
    if user.is_anonymous:
        raise _http.error.Forbidden()

    model = inp.get('model')
    language = inp.get('language', _lang.get_current())

    # User can browse ANY entities
    if user.has_permission('pytsite.odm_perm.view.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)

    # User can browse only its OWN entities
    elif user.has_permission('pytsite.odm_perm.view_own.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)
        f.where('author', '=', user)

    # User cannot browse entities, so its rights equals to the anonymous user
    else:
        f = _api.find(model, language=language)

    f.sort([('title', _odm.I_ASC)]).where('title', 'regex_i', query)
    r = [{'id': e.model + ':' + str(e.id), 'text': e.title} for e in f.get(20)]

    return {'results': r}

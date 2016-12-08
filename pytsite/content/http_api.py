"""PytSite Content HTTP API.
"""
from pytsite import http as _http, auth as _auth, lang as _lang, validation as _validation, odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def patch_view_count(**kwargs) -> int:
    """Increase content entity views counter by one.
    """
    model = kwargs.get('model')
    eid = kwargs.get('id')

    if not model:
        raise RuntimeError('Model is not specified.')

    if not eid:
        raise RuntimeError('ID is not specified.')

    if model and eid:
        entity = _api.dispense(model, eid)
        if entity:
            with entity:
                _auth.switch_user_to_system()
                entity.f_inc('views_count').save(update_timestamp=False)
                _auth.restore_user()

            return entity.views_count

    return 0


def get_widget_entity_select_search(**kwargs) -> dict:
    # Query is mandatory parameter
    query = kwargs.get('q')
    if not query:
        return {'results': ()}

    # Anonymous users cannot perform search
    user = _auth.get_current_user()
    if user.is_anonymous:
        raise _http.error.Forbidden()

    model = kwargs.get('model')
    language = kwargs.get('language', _lang.get_current())

    # User can browse ANY entities
    if user.has_permission('pytsite.odm_perm.view.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)

    # User can browse only its OWN entities
    elif user.has_permission('pytsite.odm_perm.view_own.' + model):
        f = _api.find(model, status=None, check_publish_time=None, language=language)
        f.eq('author', user.uid)

    # User cannot browse entities, so its rights equals to the anonymous user
    else:
        f = _api.find(model, language=language)

    f.sort([('title', _odm.I_ASC)]).where('title', 'regex_i', query)
    r = [{'id': e.model + ':' + str(e.id), 'text': e.title} for e in f.get(20)]

    return {'results': r}

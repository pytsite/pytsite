"""Content Plugin Endpoints.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import content as _content, disqus as _disqus, taxonomy as _taxonomy
from pytsite.core import reg as _reg, http as _http, router as _router, metatag as _metatag, assetman as _assetman, \
    odm as _odm, widget as _widget


def index(args: dict, inp: dict):
    """Content Index.
    """
    model = args.get('model')
    if not model:
        raise ValueError('Model is not specified.')

    f = _content.find(model)

    term_field = args.get('term_field')
    if term_field:
        term_model = f.mock.get_field(term_field).model
        term_alias = args.get('term_alias')
        if term_alias:
            term = _taxonomy.find(term_model).where('alias', '=', term_alias).first()
            args['term'] = term
            if isinstance(f.mock.fields[term_field], _odm.field.Ref):
                f.where(term_field, '=', term)
            elif isinstance(f.mock.fields[term_field], _odm.field.RefsListField):
                f.where(term_field, 'in', [term])
            _metatag.t_set('title', term.title)

    pager = _widget.static.Pager(f.count(), 10)

    args['entities'] = f.skip(pager.skip).get(pager.limit)
    args['pager'] = pager
    endpoint = _reg.get('content.endpoints.view.' + model, 'app.eps.' + model + '_index')

    return _router.call_endpoint(endpoint, args)


def view(args: dict, inp: dict):
    """View Content Entity.
    """
    model = args.get('model')
    entity = _content.find(model).where('_id', '=', args.get('id')).first()
    if not entity:
        raise _http.error.NotFoundError()

    current_cc = entity.f_get('comments_count')
    actual_cc = _disqus.functions.get_comments_count(_router.current_url(True))
    if actual_cc != current_cc:
        entity.f_set('comments_count', actual_cc).save()

    _metatag.t_set('title', entity.f_get('title'))

    endpoint = _reg.get('content.endpoints.view.' + model, 'app.eps.' + model + '_view')

    _assetman.add('pytsite.content@js/content.js')

    return _router.call_endpoint(endpoint, {'entity': entity})


def view_count(args: dict, inp: dict) -> int:
    model = inp.get('model')
    eid = inp.get('id')

    if model and eid:
        entity = _content.find(model).where('_id', '=', eid).first()
        if entity:
            entity.f_inc('views_count').save()
            return entity.f_get('views_count')

    return 0


def propose(args: dict, inp: dict) -> str:
    return 'TODO'


def search(args: dict, inp: dict) -> str:
    return 'TODO'

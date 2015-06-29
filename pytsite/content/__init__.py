"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    import sys
    from pytsite import admin, taxonomy
    from pytsite.core import router, assetman, events, lang, odm, tpl
    from ._model import Section

    # Dependencies
    __import__('pytsite.auth')
    __import__('pytsite.auth_ui')
    __import__('pytsite.admin')
    __import__('pytsite.image')
    __import__('pytsite.route_alias')
    __import__('pytsite.tag')

    def _section_pre_delete_handler(entity: odm.Model):
        from . import _manager
        for m in _manager.get_registered_models():
            r_entity = _manager.find(m, None, False).where('section', '=', entity).first()
            if r_entity:
                error_args = {'model': r_entity.model, 'title': r_entity.f_get('title')}
                raise odm.error.ForbidEntityDelete(lang.t('pytsite.content@referenced_entity_exists', error_args))

    lang.register_package(__name__)
    tpl.register_global('content', sys.modules[__name__])

    assetman.register_package(__name__)
    assetman.add(__name__ + '@css/common.css', '*')

    router.add_rule('/content/index/<string:model>', 'pytsite.content.eps.index')
    router.add_rule('/content/tag/<string:model>/<string:term_alias>', 'pytsite.content.eps.index', {
        'term_field': ('tags', 'tag')
    })

    router.add_rule('/content/view/<string:model>/<string:id>', 'pytsite.content.eps.view')
    router.add_rule('/content/count/<string:model>/<string:id>', 'pytsite.content.eps.view_count')

    taxonomy.register_model('section', Section, __name__ + '@sections')
    events.listen('odm.pre_delete.section', _section_pre_delete_handler)

    admin.sidebar.add_section('content', __name__ + '@content', 100, ('*',))

__init()


# Public API
from . import _manager, _model as model, _widget as widget
register_model = _manager.register_model
find = _manager.find

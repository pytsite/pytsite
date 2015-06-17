"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    from pytsite import admin, taxonomy
    from pytsite.core import router, assetman, events, lang, odm
    from ._models import SectionModel

    # Dependencies
    __import__('pytsite.auth')
    __import__('pytsite.auth_ui')
    __import__('pytsite.admin')
    __import__('pytsite.image')
    __import__('pytsite.route_alias')
    __import__('pytsite.tag')

    def _section_pre_delete_handler(entity: odm.model.ODMModel):
        from . import _manager
        for model in _manager.get_registered_models():
            r_entity = _manager.find(model, None, False).where('section', '=', entity).first()
            if r_entity:
                error_args = {'model': r_entity.model, 'title': r_entity.f_get('title')}
                raise odm.error.ForbidEntityDelete(lang.t('pytsite.content@referenced_entity_exists', error_args))

    lang.register_package(__name__)
    assetman.register_package(__name__)

    router.add_rule('/content/view/<string:model>/<string:eid>', 'pytsite.content.eps.view')

    taxonomy.manager.register_model('section', SectionModel, __name__ + '@sections')
    events.listen('odm.pre_delete.section', _section_pre_delete_handler)

    admin.sidebar.add_section('content', __name__ + '@content', 100, ('*',))

__init()


# Public API
from . import _manager
manager = _manager

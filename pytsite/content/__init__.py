"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang, router, assetman, events
from pytsite.core.odm.models import ODMModel
from pytsite.core.odm.errors import ForbidEntityDelete
from pytsite.admin import sidebar
from pytsite.taxonomy import taxonomy_manager
from .models import SectionModel

# Dependencies
__import__('pytsite.auth')
__import__('pytsite.auth_ui')
__import__('pytsite.admin')
__import__('pytsite.image')
__import__('pytsite.route_alias')
__import__('pytsite.tag')


def _section_pre_delete_handler(entity: ODMModel):
    from . import content_manager
    for model in content_manager.get_registered_models():
        r_entity = content_manager.find(model, None, False).where('section', '=', entity).first()
        if r_entity:
            error_args = {'model': r_entity.model, 'title': r_entity.f_get('title')}
            raise ForbidEntityDelete(lang.t('pytsite.content@referenced_entity_exists', error_args))

lang.register_package(__name__)
assetman.register_package(__name__)

router.add_rule('/content/view/<string:model>/<string:eid>', 'pytsite.content.eps.view')

taxonomy_manager.register_model('section', SectionModel)
events.listen('odm.pre_delete.section', _section_pre_delete_handler)


sidebar.add_section('content', lang.t(__name__ + '@content'), 100, ('*',))

"""PytSite Content Import Package.
"""
# Public API
from ._api import register_driver, get_driver, get_drivers
from . import _driver as driver, _model as model, _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import odm, lang, admin, router, events, permissions
    from . import _model, _api, _driver, _eh

    # Resources
    lang.register_package(__name__)

    permissions.define_group('content_import', 'pytsite.content_import@content_import')

    odm.register_model('content_import', _model.ContentImport)

    # Event handlers
    events.listen('pytsite.odm.model.setup_indexes', _eh.odm_model_setup_indexes)
    events.listen('pytsite.cron.1min', _eh.cron_1min)

    # Sidebar menu
    m = 'content_import'
    admin.sidebar.add_menu(sid='content', mid=m, title=__name__ + '@import',
                           href=router.ep_path('pytsite.odm_ui@browse', {'model': m}),
                           icon='fa fa-download',
                           permissions=('pytsite.odm_perm.view.' + m, 'pytsite.odm_perm.view_own.' + m),
                           weight=110)

    # RSS import driver
    _api.register_driver(_driver.RSS())

__init()

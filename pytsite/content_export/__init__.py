"""PytSite Content Export Plugin.
"""
# Public API
from . import _model as model, _error as error
from ._driver import Abstract as AbstractDriver
from ._api import register_driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import admin, odm, events, lang, router, permissions
    from . import _model, _eh

    permissions.define_group('content_export', 'pytsite.content_export@content_export')

    # Resources
    lang.register_package(__name__)

    # ODM models
    odm.register_model('content_export', _model.ContentExport)

    # Event handlers
    events.listen('pytsite.cron.1min', _eh.cron_1min)

    # Sidebar menu
    m = 'content_export'
    admin.sidebar.add_menu(sid='content', mid=m, title=__name__ + '@export',
                           href=router.ep_path('pytsite.odm_ui@browse', {'model': m}),
                           icon='fa fa-bullhorn',
                           permissions=('pytsite.odm_perm.view.' + m, 'pytsite.odm_perm.view_own.' + m),
                           weight=100)

__init()

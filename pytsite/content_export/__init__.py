"""PytSite Content Export Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Dependencies
__import__('pytsite.content')


def __init():
    """Init wrapper.
    """
    from pytsite import admin
    from pytsite.core import router, odm, lang, events
    from ._model import ContentExport
    from ._functions import cron_15m_event_handler

    # Resources
    lang.register_package(__name__)

    # ODM models
    odm.register_model('content_export', ContentExport)

    # Event handlers
    events.listen('pytsite.core.cron.15min', cron_15m_event_handler)

    m = 'content_export'
    admin.sidebar.add_menu('misc', m, __name__ + '@export',
                           href=router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': m}),
                           icon='fa fa-bullhorn',
                           permissions=('pytsite.odm_ui.browse.' + m,'pytsite.odm_ui.browse_own.' + m))

__init()


# Public API
from . import _model as model
from ._driver import Abstract as AbstractDriver
from ._functions import register_driver

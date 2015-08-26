"""Flag Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite import assetman
    from pytsite import odm
    from pytsite import events
    from pytsite import tpl
    from pytsite import lang
    from . import _model

    def router_dispatch_eh():
        assetman.add('pytsite.flag@css/common.css')
        assetman.add('pytsite.flag@js/common.js')

    lang.register_package(__name__)
    assetman.register_package(__name__)
    tpl.register_package(__name__)
    tpl.register_global('flag', sys.modules[__package__])
    odm.register_model('flag', _model.Flag)

    events.listen('pytsite.router.dispatch', router_dispatch_eh)

__init()


# Public API
from . import _widget as widget
from ._functions import count

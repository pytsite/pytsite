"""PytSite JS API.
"""
# Public API
from ._api import include, is_ep_registered, register_ep

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, router, tpl

    router.add_rule('/pytsite/browser/<string:ep>', 'pytsite.browser.ep.request', methods=('GET', 'POST'))

    assetman.register_package(__name__)

    assetman.add(__name__ + '@js/jquery-2.1.4.min.js', forever=True)
    assetman.add(__name__ + '@js/common.js', forever=True)
    assetman.add(__name__ + '@js/lang.js', forever=True)
    assetman.add('app@js/translations.js', forever=True)

    tpl.register_global('browser_include', include)


__init()

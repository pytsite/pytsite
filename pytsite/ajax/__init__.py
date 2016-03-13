"""PytSite AJAX API.
"""
# Public API
from ._api import is_ep_registered, register_ep

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import router, assetman

    router.add_rule('/pytsite/ajax/<string:ep>', 'pytsite.ajax.ep.request', methods=('GET', 'POST'))

    assetman.register_package(__name__)
    assetman.add(__name__ + '@js/ajax.js', permanent=True)

__init()

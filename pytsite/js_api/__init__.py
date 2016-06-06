"""PytSite AJAX API.
"""
# Public API
from ._api import ep_url

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import router, assetman

    router.add_rule('/pytsite/js_api/<endpoint>', 'pytsite.js_api@entry', methods=('GET', 'POST'))

    assetman.register_package(__name__)
    assetman.add(__name__ + '@js/common.js', permanent=True)

__init()

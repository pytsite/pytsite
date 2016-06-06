"""PytSite JS API Functions.
"""
from pytsite import router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def ep_url(js_api_ep_name) -> str:
    """Construct JS API endpoint URL.
    """
    return _router.ep_url('pytsite.js_api@entry', {'endpoint': js_api_ep_name})

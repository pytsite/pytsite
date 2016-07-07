"""PytSite ODM UI HTTP API Endpoints.
"""
from pytsite import http as _http
from . import _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_browser_rows(inp: dict) -> list:
    """Get browser rows via AJAX request.
    """
    model = inp.get('model')
    offset = int(inp.get('offset', 0))
    limit = int(inp.get('limit', 0))
    sort_field = inp.get('sort')
    sort_order = inp.get('order')
    search = inp.get('search')
    browser = _browser.Browser(model)
    rows = browser.get_rows(offset, limit, sort_field, sort_order, search)

    return rows

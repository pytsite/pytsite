"""PytSite ODM UI HTTP API Endpoints.
"""
from . import _browser

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_browser_rows(**kwargs) -> list:
    """Get browser rows via AJAX request.
    """
    model = kwargs.get('model')
    offset = int(kwargs.get('offset', 0))
    limit = int(kwargs.get('limit', 0))
    sort_field = kwargs.get('sort')
    sort_order = kwargs.get('order')
    search = kwargs.get('search')
    browser = _browser.Browser(model)
    rows = browser.get_rows(offset, limit, sort_field, sort_order, search)

    return rows

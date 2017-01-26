"""PytSite ODM HTTP API.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import http_api
    from . import _http_api

    http_api.handle('POST', 'odm/<model>', _http_api.post_entity, 'pytsite.odm@post_entity')
    http_api.handle('GET', 'odm/<model>/<uid>', _http_api.get_entity, 'pytsite.odm@get_entity')
    http_api.handle('PATCH', 'odm/<model>/<uid>', _http_api.patch_entity, 'pytsite.odm@patch_entity')
    http_api.handle('DELETE', 'odm/<model>/<uid>', _http_api.delete_entity, 'pytsite.odm@delete_entity')


_init()

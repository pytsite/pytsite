"""PytSite ODM HTTP API
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import http_api, assetman
    from . import _http_api_controllers

    http_api.handle('GET', 'odm/entities/<model>', _http_api_controllers.GetEntities(),
                    'pytsite.odm_http_api@get_entities')

    http_api.handle('POST', 'odm/entity/<model>', _http_api_controllers.PostEntity(),
                    'pytsite.odm_http_api@post_entity')
    http_api.handle('GET', 'odm/entity/<model>/<uid>', _http_api_controllers.GetEntity(),
                    'pytsite.odm_http_api@get_entity')
    http_api.handle('PATCH', 'odm/entity/<model>/<uid>', _http_api_controllers.PatchEntity(),
                    'pytsite.odm_http_api@patch_entity')
    http_api.handle('DELETE', 'odm/entity/<model>/<uid>', _http_api_controllers.DeleteEntity(),
                    'pytsite.odm_http_api@delete_entity')

    # JavaScript API
    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.js_module('odm-http-api', __name__ + '@odm-http-api')



_init()

"""PytSite ODM HTTP API
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import http_api, assetman
    from . import _controllers

    http_api.handle('GET', 'odm/entities/<model>', _controllers.GetEntities(),
                    'pytsite.odm_http_api@get_entities')

    http_api.handle('POST', 'odm/entity/<model>', _controllers.PostEntity(),
                    'pytsite.odm_http_api@post_entity')
    http_api.handle('GET', 'odm/entity/<model>/<uid>', _controllers.GetEntity(),
                    'pytsite.odm_http_api@get_entity')
    http_api.handle('PATCH', 'odm/entity/<model>/<uid>', _controllers.PatchEntity(),
                    'pytsite.odm_http_api@patch_entity')
    http_api.handle('DELETE', 'odm/entity/<model>/<uid>', _controllers.DeleteEntity(),
                    'pytsite.odm_http_api@delete_entity')

    # JavaScript API
    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.js_module('odm-http-api', __name__ + '@odm-http-api')



_init()

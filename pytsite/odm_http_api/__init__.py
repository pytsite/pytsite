"""PytSite ODM HTTP API.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import http_api

    http_api.register_handler('odm', 'pytsite.odm_http_api.http_api')


_init()

"""PytSite HTTP API Package.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import router
    from . import ep

    router.add_rule('/api/<int:version>/<string:package>/<string:callback>', 'pytsite.http_api.ep.entry')


_init()

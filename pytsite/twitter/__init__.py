"""Twitter Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    from pytsite import oauth, poster
    from pytsite.core import lang
    from ._oauth import Driver as OAuthDriver
    from ._poster import Driver as PosterDriver

    lang.register_package(__name__)

    oauth.register_driver('twitter', lang.t('pytsite.twitter@twitter'), OAuthDriver)
    poster.register_driver('twitter', lang.t('pytsite.twitter@twitter'), PosterDriver)

__init()

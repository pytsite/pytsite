"""Twitter Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Dependencies
__import__('pytsite.oauth')


def __init():
    from pytsite import oauth
    from pytsite.core import lang
    from ._oauth import Driver as OAuthDriver

    lang.register_package(__name__)
    oauth.register_driver('twitter', lang.t('pytsite.twitter@twitter'), OAuthDriver)

__init()

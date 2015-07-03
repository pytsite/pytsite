"""Twitter Poster Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import poster as _poster


class Driver(_poster.AbstractDriver):
    def create_post(self, **kwargs: dict):
        pass

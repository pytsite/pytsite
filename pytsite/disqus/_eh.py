"""Disqus Package Event Handlers.
"""
from pytsite import db as _db, console as _console

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def pytsite_update(version: str):
    """'pytsite.update' event handler.
    """
    if version == '0.47.0':
        # Drop 'disqus_comment_counts' because it doesn't needed anymore
        _db.get_collection('disqus_comment_counts').drop()
        _console.print_info("'disqus_comment_counts' collection has been dropped.")

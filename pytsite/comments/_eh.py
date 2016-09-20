"""Event Handlers.
"""
from pytsite import db as _db

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def update(version: str):
    """'pytsite.update' event handler.
    """
    if version == '0.73.0':
        # Not needed anymore
        _db.get_collection('comments_counts').drop()

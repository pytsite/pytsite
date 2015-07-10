"""Page Plugin Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import content as _content


def replace_model(cls):
    """Replace page model's class.
    """
    _content.register_model('page', cls, 'page@pages', replace=True)

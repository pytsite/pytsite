"""PytSite Block API.
"""
from pytsite import content as _content
from . import _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_block(uid: str, language: str = None, exception: bool = True) -> _model.Block:
    """Get block by UID.
    """
    block = _content.find('block', language=language).eq('uid', uid).first()
    if not block and exception:
        raise _error.BlockNotFound("Block '{}' is not found.".format(uid))

    return block

"""PytSite Comments Native Driver.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import comments, odm, odm_perm
    from . import _model, _driver

    # Register ODM model
    odm.register_model('comment_native', _model.Comment)

    # Additional ODM permissions
    odm_perm

    # Register comments driver
    comments.register_driver(_driver.Native())


_init()

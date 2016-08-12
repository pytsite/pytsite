"""PytSite Comments ODM Driver.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import comments, odm, tpl, assetman, events
    from . import _model, _driver, _eh

    # Register ODM model
    odm.register_model('comment', _model.Comment)

    # Register comments driver
    comments.register_driver(_driver.Native())

    # Resources
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    events.listen('pytsite.setup', _eh.setup)
    events.listen('pytsite.comments.report_comment', _eh.comments_report_comment)


_init()

"""PytSite Content Import Event Handlers.
"""
from frozendict import frozendict as _frozendict
from pytsite import odm as _odm, logger as _logger
from . import _api, _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_1min():
    """'pytsite.cron.1min' event handler.
    """
    f = _odm.find('content_import').where('enabled', '=', True)
    for ci in f.get():  # type: _model.ContentImport
        options = dict(ci.driver_options)
        options.update({
            'content_author': ci.content_author,
            'content_model': ci.content_model,
            'content_language': ci.content_language,
            'content_status': ci.content_status,
            'content_section': ci.content_section,
            'with_images_only': ci.with_images_only,
            'add_tags': ci.add_tags,
        })

        driver = _api.get_driver(ci.driver)
        max_items = 1
        items_imported = 0
        try:
            _logger.info('Content import started.', __name__)

            for e in driver.get_entities(_frozendict(options)):
                if items_imported == max_items:
                    break

                e.save()
                _logger.info("Content entity imported: '{}'".format(e.title), __name__)

                items_imported += 1

            _logger.info('Content import finished. Entities imported: {}.'.format(items_imported), __name__)

        except _error.ImportError as e:
            _logger.error('Import error: {}.'.format(str(e)), __name__)

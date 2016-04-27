"""PytSite Content Import Event Handlers.
"""
from datetime import datetime as _datetime, timedelta as _timedelta
from frozendict import frozendict as _frozendict
from pytsite import odm as _odm, logger as _logger, content as _content, reg as _reg
from . import _api, _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def odm_model_setup_indexes(entity: _odm.Entity):
    if isinstance(entity, _content.model.Content):
        entity.define_field(_odm.field.Dict('content_import'))
        entity.define_index([('content_import.source_domain', _odm.I_ASC)])


def cron_1min():
    """'pytsite.cron.1min' event handler.
    """
    max_errors = _reg.get('content_import.max_errors', 13)
    delay_errors = _reg.get('content_export.delay_errors', 120)

    importer_finder = _odm.find('content_import') \
        .where('enabled', '=', True) \
        .where('paused_till', '<', _datetime.now()) \
        .sort([('errors', _odm.I_ASC)])

    for importer in importer_finder.get():  # type: _model.ContentImport
        options = dict(importer.driver_opts)
        options.update({
            'content_author': importer.content_author,
            'content_model': importer.content_model,
            'content_language': importer.content_language,
            'content_status': importer.content_status,
            'content_section': importer.content_section,
            'with_images_only': importer.with_images_only,
        })

        driver = _api.get_driver(importer.driver)
        max_items = 20
        items_imported = 0
        try:
            _logger.info('Content import started. Driver: {}. Options: {}'.format(driver.get_name(), options), __name__)

            for e in driver.get_entities(_frozendict(options)):
                if items_imported == max_items:
                    break

                # Append tags
                for tag_title in importer.add_tags:
                    e.f_add('tags', _content.dispense_tag(tag_title).save())

                # Save entity
                e.save()
                _logger.info("Content entity imported: '{}'".format(e.title), __name__)
                items_imported += 1

            _logger.info('Content import finished. Entities imported: {}.'.format(items_imported), __name__)

        except _error.ContentImportError as e:
            # Increment errors counter
            importer.f_inc('errors')

            # Store info about error
            importer.f_set('last_error', str(e))

            if importer.errors >= max_errors:
                # Disable if maximum errors count reached
                importer.f_set('enabled', False)
            else:
                # Pausing importer
                importer.f_set('paused_till', _datetime.now() + _timedelta(minutes=delay_errors))

            _logger.error('Import error: {}.'.format(str(e)), __name__)

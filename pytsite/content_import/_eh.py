"""PytSite Content Import Event Handlers.
"""
from datetime import datetime as _datetime, timedelta as _timedelta
from frozendict import frozendict as _frozendict
from pytsite import odm as _odm, logger as _logger, content as _content, reg as _reg, events as _events
from . import _api, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def odm_model_setup_indexes(entity: _odm.model.Entity):
    if isinstance(entity, _content.model.Content):
        entity.define_field(_odm.field.Dict('content_import'))
        entity.define_index([('content_import.source_domain', _odm.I_ASC)])


def cron_1min():
    """'pytsite.cron.1min' event handler.
    """
    max_errors = _reg.get('content_import.max_errors', 13)
    delay_errors = _reg.get('content_export.delay_errors', 120)

    importer_finder = _odm.find('content_import') \
        .eq('enabled', True) \
        .lt('paused_till', _datetime.now()) \
        .sort([('errors', _odm.I_ASC)])

    for importer in importer_finder.get():  # type: _model.ContentImport
        options = dict(importer.driver_opts)
        options.update({
            'content_author': importer.content_author,
            'content_model': importer.content_model,
            'content_language': importer.content_language,
            'content_status': importer.content_status,
            'content_section': importer.content_section,
        })

        driver = _api.get_driver(importer.driver)
        max_items = 1
        items_imported = 0
        try:
            importer.lock()
            _logger.info('Content import started. Driver: {}. Options: {}'.format(driver.get_name(), options))

            # Get entities from driver and save them
            for entity in driver.get_entities(_frozendict(options)):
                if items_imported == max_items:
                    break

                try:
                    entity.lock()

                    # Append additional tags
                    if entity.has_field('tags'):
                        for tag_title in importer.add_tags:
                            tag = _content.dispense_tag(tag_title)
                            with tag:
                                tag.save()
                                entity.f_add('tags', tag)

                    # Save entity
                    entity.save()

                    # Notify listeners
                    _events.fire('pytsite.content_import.import', driver=driver, entity=entity)

                    _logger.info("Content entity imported: '{}'".format(entity.f_get('title')))
                    items_imported += 1

                # Entity was not successfully saved; make record in the log and skip to the next entity
                except Exception as e:
                    # Delete already attached images to free space
                    if entity.has_field('images') and entity.images:
                        for img in entity.images:
                            img.delete()

                    _logger.warn("Error while creating entity '{}'. {}".format(entity.title, str(e)))

                finally:
                    entity.unlock()

            # Mark that driver made its work without errors
            importer.f_set('errors', 0)

            _logger.info('Content import finished. Entities imported: {}.'.format(items_imported))

        except Exception as e:
            # Increment errors counter
            importer.f_inc('errors')

            # Store info about error
            importer.f_set('last_error', str(e))

            if importer.errors >= max_errors:
                # Disable if maximum errors count reached
                importer.f_set('enabled', False)
            else:
                # Pause importer
                importer.f_set('paused_till', _datetime.now() + _timedelta(minutes=delay_errors))

            _logger.error(str(e), exc_info=e)

            # Continue to the next importer
            continue

        finally:
            importer.save()
            importer.unlock()

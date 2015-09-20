"""Event Handlers.
"""
import hashlib as _hashlib
import pytz as _pytz
from os import path as _path, makedirs as _makedirs
from shutil import rmtree as _rmtree
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import settings as _settings, sitemap as _sitemap, feed as _feed, reg as _reg, logger as _logger, \
    tpl as _tpl, mail as _mail, odm as _odm, lang as _lang, router as _router, metatag as _metatag, \
    console as _console
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_hourly():
    """'pytsite.cron.hourly' event handler.
    """
    _generate_feeds()


def cron_daily():
    """'pytsite.cron.daily' event handler.
    """
    _generate_sitemap()


def cron_weekly():
    """'pytsite.cron.weekly' event handler.
    """
    _mail_digest()


def router_dispatch():
    """'pytsite.router.dispatch' Event Handler.
    """
    if not _router.is_base_url():
        return

    lng = _lang.get_current_lang()
    settings = _settings.get_setting('content')

    for s_key in ['title', 'description', 'keywords']:
        s_full_key = 'home_{}_{}'.format(s_key, lng)
        if s_full_key in settings:
            s_val = settings[s_full_key]
            if isinstance(s_val, list):
                s_val = ','.join(s_val)
            _metatag.t_set(s_key, s_val)

            if s_key in ['title', 'description']:
                _metatag.t_set('og:' + s_key, s_val)
                _metatag.t_set('twitter:' + s_key, s_val)


def update(version: str):
    if version == '0.7.0':
        _update_0_7_0()


def _mail_digest():
    """Mail weekly mail digest.
    """
    model = _reg.get('content.digest.model')
    if not model:
        return

    _logger.info('Weekly mail digest start.', __name__)

    for subscriber in _odm.find('content_subscriber').where('enabled', '=', True).get():
        content_f = _functions.find(model).where('publish_time', '>', _datetime.now() - _timedelta(7))
        content_f.sort([('views_count', _odm.I_DESC)])
        m_body = _tpl.render(_reg.get('content.digest.tpl', 'mail/digest'), {
            'entities': content_f.get(_reg.get('content.digest.num', 10)),
            'subscriber': subscriber
        })
        _mail.Message(subscriber.f_get('email'), _lang.t('pytsite.content@weekly_digest_mail_subject'), m_body).send()

    _logger.info('Weekly mail digest stop.', __name__)


def _generate_sitemap():
    """Generate content sitemap.
    """
    _logger.info('Sitemap generation start.', __name__)

    output_dir = _path.join(_reg.get('paths.static'), 'sitemap')
    if _path.exists(output_dir):
        _rmtree(output_dir)
    _makedirs(output_dir, 0o755, True)

    sitemap_index = _sitemap.Index()
    links_per_file = 50000
    loop = 1
    loop_links = 1
    sitemap = _sitemap.Sitemap()
    sitemap.add_url(_router.base_url(), _datetime.now(), 'always', 1)
    for model in _reg.get('content.sitemap.models', []):
        _logger.info("Sitemap generation started for model '{}'.".format(model), __name__)
        for entity in _functions.find(model).get():
            sitemap.add_url(entity.url, entity.publish_time)
            loop_links += 1
            if loop_links >= links_per_file:
                loop += 1
                loop_links = 0
                sitemap_path = sitemap.write(_path.join(output_dir, 'data-%02d.xml' % loop), True)
                _logger.info("'{}' successfully written with {} links.".format(sitemap_path, loop_links), __name__)
                sitemap_index.add_url(_router.url('/sitemap/{}'.format(_path.basename(sitemap_path))))
                del sitemap
                sitemap = _sitemap.Sitemap()

        if len(sitemap):
            sitemap_path = sitemap.write(_path.join(output_dir, 'data-%02d.xml' % loop), True)
            _logger.info("'{}' successfully written with {} links.".format(sitemap_path, loop_links), __name__)
            sitemap_index.add_url(_router.url('/sitemap/{}'.format(_path.basename(sitemap_path))))
            del sitemap

    if len(sitemap_index):
        sitemap_index_path = sitemap_index.write(_path.join(output_dir, 'index.xml'))
        _logger.info("'{}' successfully written.".format(sitemap_index_path), __name__)

    _logger.info('Sitemap generation stop.', __name__)


def _generate_feeds():
    output_dir = _path.join(_reg.get('paths.static'), 'feed')
    if _path.exists(output_dir):
        _rmtree(output_dir)
    _makedirs(output_dir, 0o755, True)

    md5 = _hashlib.md5()
    feed_length = _reg.get('content.feed.length', 20)
    content_settings = _settings.get_setting('content')
    for lang in _lang.get_langs():
        feed_title = content_settings.get('home_title_' + lang)
        feed_description = content_settings.get('home_description_' + lang)
        for model in _reg.get('content.feed.models', []):
            _logger.info("Feeds generation started for model '{}', language '{}'.".format(model, lang), __name__)
            feed_writer = _feed.Writer(feed_title, _router.base_url(), feed_description)
            for entity in _functions.find(model).get(feed_length):
                entry = feed_writer.add_entry()

                md5.update(entity.title.encode())
                entry.id(md5.hexdigest())
                entry.title(entity.title)
                entry.content(entity.description, type='text/plain')
                entry.link({'href': entity.url})

                tz = _pytz.timezone(_reg.get('server.timezone', 'UTC'))
                entry.pubdate(tz.localize(entity.publish_time))

                author_info = {
                    'name': entity.author.full_name,
                    'email': entity.author.email,
                }
                if entity.author.profile_is_public:
                    author_info['uri'] = _router.ep_url('pytsite.auth_ui.ep.profile_view', {
                        'nickname': str(entity.author.nickname),
                    })
                entry.author(author_info)

                if entity.has_field('section'):
                    entry.category({
                        'term': entity.section.alias,
                        'label': entity.section.title,
                    })

                if entity.has_field('tags'):
                    for tag in entity.tags:
                        entry.category({
                            'term': tag.alias,
                            'label': tag.title,
                        })

            for out_type in 'rss', 'atom':
                out_path = _path.join(output_dir, '{}-{}-{}.xml'.format(out_type, model, lang))
                if out_type == 'rss':
                    feed_writer.rss_file(out_path, True)
                    _logger.info("RSS feed successfully written to '{}'.".format(out_path), __name__)
                if out_type == 'atom':
                    feed_writer.atom_file(out_path, True)
                    _logger.info("Atom feed successfully written to '{}'.".format(out_path), __name__)


def _update_0_7_0():
    for lang_code in _lang.get_langs():
        for model in _functions.get_models().keys():
            for entity in _functions.find(model, None, False, lang_code).get():
                # Updating only entities without 'language_db' field
                if entity.f_get('language_db'):
                    continue

                msg = "Updating content entity: model='{}', language='{}', id='{}'".\
                    format(model, lang_code, entity.id)
                _logger.info(msg, __name__)
                _console.print_info(msg)
                entity.save()

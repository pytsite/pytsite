"""Event Handlers.
"""
from os import path as _path, makedirs as _makedirs
from shutil import rmtree as _rmtree
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import settings as _settings, sitemap as _sitemap, reg as _reg, logger as _logger, tpl as _tpl, \
    mail as _mail, odm as _odm, lang as _lang, router as _router, metatag as _metatag, assetman as _assetman
from . import _api

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
    settings = _settings.get_setting('content')

    # Add inline JS code
    if 'add_js' in settings and settings['add_js']:
        _assetman.add_inline(settings['add_js'])

    # Add meta tags for home page
    if _router.is_base_url():
        lng = _lang.get_current()
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


def _mail_digest():
    """Send weekly mail digest.
    """
    model = _reg.get('content.digest.model')
    if not model:
        return

    app_name = _lang.t('app_name')
    entities_num = _reg.get('content.digest.num', 10)

    for lng in _lang.langs():
        _logger.info("Weekly mail digest for language {} started.".format(lng))

        m_subject = _lang.t('pytsite.content@weekly_digest_mail_subject', {'app_name': app_name}, lng)
        f = _odm.find('content_subscriber').where('enabled', '=', True).where('language', '=', lng)
        for subscriber in f.get():
            content_f = _api.find(model, language=lng)
            content_f.where('publish_time', '>', _datetime.now() - _timedelta(7))
            content_f.sort([('views_count', _odm.I_DESC)])
            m_body = _tpl.render(_reg.get('content.digest.tpl', 'mail/content/digest'), {
                'entities': content_f.get(entities_num),
                'subscriber': subscriber,
                'language': lng,
            })
            msg = _mail.Message(subscriber.f_get('email'), m_subject, m_body)
            msg.send()

        _logger.info("Weekly mail digest for language {} finished.".format(lng))


def _generate_sitemap():
    """Generate content sitemap.
    """
    _logger.info('Sitemap generation start.')

    output_dir = _path.join(_reg.get('paths.static'), 'sitemap')
    if _path.exists(output_dir):
        _rmtree(output_dir)
    _makedirs(output_dir, 0o755, True)

    sitemap_index = _sitemap.Index()
    links_per_file = 50000
    loop_count = 1
    loop_links = 1
    sitemap = _sitemap.Sitemap()
    sitemap.add_url(_router.base_url(), _datetime.now(), 'always', 1)
    for lang in _lang.langs():
        for model in _reg.get('content.sitemap.models', []):
            _logger.info("Sitemap generation started for model '{}', language '{}'.".
                         format(model, _lang.lang_title(lang)))

            for entity in _api.find(model, language=lang).get():
                sitemap.add_url(entity.url, entity.publish_time)
                loop_links += 1

                # Flush sitemap
                if loop_links >= links_per_file:
                    loop_count += 1
                    loop_links = 0
                    sitemap_path = sitemap.write(_path.join(output_dir, 'data-%02d.xml' % loop_count), True)
                    _logger.info("'{}' successfully written with {} links.".format(sitemap_path, loop_links))
                    sitemap_index.add_url(_router.url('/sitemap/{}'.format(_path.basename(sitemap_path))))
                    del sitemap
                    sitemap = _sitemap.Sitemap()

    # If non-flushed sitemap exist
    if len(sitemap):
        sitemap_path = sitemap.write(_path.join(output_dir, 'data-%02d.xml' % loop_count), True)
        _logger.info("'{}' successfully written with {} links.".format(sitemap_path, loop_links))
        sitemap_index.add_url(_router.url('/sitemap/{}'.format(_path.basename(sitemap_path))))

    if len(sitemap_index):
        sitemap_index_path = sitemap_index.write(_path.join(output_dir, 'index.xml'))
        _logger.info("'{}' successfully written.".format(sitemap_index_path))

    _logger.info('Sitemap generation stop.')


def _generate_feeds():
    # For each language we have separate feed
    for lng in _lang.langs():
        # Generate RSS feed for each model
        for model in _reg.get('content.feed.models', ()):
            filename = 'rss-{}'.format(model)
            _api.generate_rss(model, filename, lng, length=_reg.get('content.feed.length', 20))

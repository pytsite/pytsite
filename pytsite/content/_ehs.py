"""Event Handlers.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path as _path, makedirs as _makedirs
from shutil import rmtree as _rmtree
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import settings as _settings, sitemap as _sitemap
from pytsite.core import reg as _reg, logger as _logger, tpl as _tpl, mail as _mail, odm as _odm, lang as _lang, \
    router as _router, metatag as _metatag
from . import _functions


def cron_daily():
    """'pytsite.core.cron.daily' event handler.
    """
    _generate_sitemap()


def cron_weekly():
    """'pytsite.core.cron.weekly' event handler.
    """
    _mail_digest()


def router_dispatch():
    """'pytsite.core.router.dispatch' Event Handler.
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


def _mail_digest():
    """Mail weekly mail digest.
    """
    model = _reg.get('content.digest.model')
    if not model:
        return

    _logger.info(__name__ + '. Weekly mail digest start.')

    for subscriber in _odm.find('content_subscriber').where('enabled', '=', True).get():
        content_f = _functions.find(model).where('publish_time', '>', _datetime.now() - _timedelta(7))
        content_f.sort([('views_count', _odm.I_DESC)])
        m_body = _tpl.render(_reg.get('content.digest.tpl', 'mail/digest'), {
            'entities': content_f.get(_reg.get('content.digest.num', 10)),
            'subscriber': subscriber
        })
        _mail.Message(subscriber.f_get('email'), _lang.t('pytsite.content@weekly_digest_mail_subject'), m_body).send()

    _logger.info(__name__ + '. Weekly mail digest stop.')


def _generate_sitemap():
    """Generate content sitemap.
    """
    _logger.info(__name__ + '. Sitemap generation start.')

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
        _logger.info(__name__ + ". Sitemap generation started for model '{}'.".format(model))
        for entity in _functions.find(model).get():
            sitemap.add_url(entity.url, entity.publish_time)
            loop_links += 1
            if loop_links >= links_per_file:
                loop += 1
                loop_links = 0
                sitemap_path = sitemap.write(_path.join(output_dir, 'data-%02d.xml' % loop), True)
                _logger.info(__name__ + ". '{}' successfully written with {} links.".format(sitemap_path, loop_links))
                sitemap_index.add_url(_router.url('/sitemap/{}'.format(_path.basename(sitemap_path))))
                del sitemap
                sitemap = _sitemap.Sitemap()

        if len(sitemap):
            sitemap_path = sitemap.write(_path.join(output_dir, 'data-%02d.xml' % loop), True)
            _logger.info(__name__ + ". '{}' successfully written with {} links.".format(sitemap_path, loop_links))
            sitemap_index.add_url(_router.url('/sitemap/{}'.format(_path.basename(sitemap_path))))
            del sitemap

    if len(sitemap_index):
        sitemap_index_path = sitemap_index.write(_path.join(output_dir, 'index.xml'))
        _logger.info(__name__ + ". '{}' successfully written.".format(sitemap_index_path))

    _logger.info(__name__ + '. Sitemap generation stop.')

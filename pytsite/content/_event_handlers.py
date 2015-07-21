"""Event Handlers.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import settings as _settings
from pytsite.core import reg as _reg, logger as _logger, tpl as _tpl, mail as _mail, odm as _odm, lang as _lang, \
    router as _router, metatag as _metatag
from . import _functions


def cron_weekly():
    """'pytsite.core.cron.weekly' event handler.
    """
    _mail_digest()


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
        _logger.info(__name__ + '. Digest has been sent to ' + subscriber.f_get('email'))

    _logger.info(__name__ + '. Weekly mail digest stop.')


def router_dispatch():
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
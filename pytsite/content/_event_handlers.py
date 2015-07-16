"""Event Handlers.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite.core import reg as _reg, logger as _logger, tpl as _tpl, mail as _mail, odm as _odm
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

    f = _functions.find(model).where('publish_time', '>', _datetime.now() - _timedelta(7))
    f.sort([('views_count', _odm.I_DESC)])
    m_body = _tpl.render(_reg.get('content.digest.tpl', 'mail/digest'), {
        'entities': f.get(_reg.get('content.digest.num', 10))
    })

    print(m_body)
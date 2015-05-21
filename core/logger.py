"""PytSite Logger.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path, makedirs
from datetime import datetime
import logging
from . import reg


_log_dir = reg.get('paths.log')
_now = datetime.now()
_log_path = path.join(_log_dir, _now.strftime('%Y%m%d.log'))

if not path.exists(_log_dir):
    makedirs(_log_dir, 0o755, True)

_format='%(asctime)s %(name)s %(levelname)-8s "%(message)s" at %(url)s'
logging.basicConfig(filename=_log_path, datefmt='%Y-%m-%d %H:%M:%S', format=_format)
_logger = logging.getLogger(reg.get('env.name', 'default'))


def info(msg: str, *args, **kwargs):
    if 'extra' not in kwargs:
        kwargs['extra'] = {}

    from . import router
    kwargs['extra']['url'] = router.current_url()

    _logger.info(msg, *args, **kwargs)

def error(msg: str, *args, **kwargs):
    if 'extra' not in kwargs:
        kwargs['extra'] = {}

    from . import router
    kwargs['extra']['url'] = router.current_url()

    kwargs['exc_info'] = True
    _logger.error(msg, *args, **kwargs)

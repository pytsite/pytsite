"""PytSite Logger
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from ._api import debug, info, warn, error


def _init():
    import logging

    from os import path, makedirs
    from datetime import datetime
    from pytsite import reg, cleanup

    _log_dir = reg.get('paths.log')
    _log_path = path.join(_log_dir, datetime.now().strftime('{}-%Y%m%d.log'.format(reg.get('env.type'))))
    _log_level = logging.DEBUG if reg.get('debug') else logging.INFO

    if not path.exists(_log_dir):
        makedirs(_log_dir, 0o755, True)

    # Create logger
    logger = logging.getLogger(reg.get('env.name', 'default'))
    logger.setLevel(_log_level)

    # Setup handler
    _handler = logging.FileHandler(_log_path, encoding='utf-8')
    if _log_level == logging.DEBUG:
        fmt = '%(asctime)s %(levelname)7s %(process)d:%(thread)d %(message)s'
    else:
        fmt = '%(asctime)s %(levelname)7s %(message)s'
    _handler.setFormatter(logging.Formatter(fmt))
    _handler.setLevel(_log_level)
    logger.addHandler(_handler)

    # Events handlers
    from . import _eh
    cleanup.on_cleanup(_eh.cleanup)


_init()

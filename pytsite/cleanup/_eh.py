"""PytSite Cleanup Console Commands.
"""
import time as _time
from os import listdir as _listdir, path as _path, unlink as _unlink
from pytsite import logger as _logger, reg as _reg, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_hourly():
    _clean_tmp_files()
    _clean_sessions()


def _clean_tmp_files():
    tmp_dir = _reg.get('paths.tmp')

    _logger.info('Cleaning up temporary files in {}'.format(tmp_dir), __name__)

    for file_name in _listdir(tmp_dir):
        file_path = _path.join(tmp_dir, file_name)
        if _path.isfile(file_path) and (_time.time() - _path.getmtime(file_path)) >= 1800:  # 30 min
            _logger.info('Removing {}'.format(file_path), __name__)
            _unlink(file_path)


def _clean_sessions():
    ttl = int(_reg.get('router.session.ttl', 21600))  # 6 hours
    _logger.info('Cleaning up old session data in {}'.format(_router.session_storage_path), __name__)

    for file_name in _listdir(_router.session_storage_path):
        file_path = _path.join(_router.session_storage_path, file_name)
        if _path.isfile(file_path) and (_time.time() - _path.getmtime(file_path)) >= ttl:
            _logger.info('Removing {}'.format(file_path), __name__)
            _unlink(file_path)

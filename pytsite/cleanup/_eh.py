"""PytSite Cleanup Event Handlers
"""
import time as _time
from os import listdir as _listdir, path as _path, unlink as _unlink
from pytsite import logger as _logger, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_hourly():
    _cleanup_tmp_files()
    _cleanup_sessions()


def _cleanup_tmp_files():
    tmp_dir = _reg.get('paths.tmp')

    _logger.info('Cleaning up temporary files in {}'.format(tmp_dir))

    for file_name in _listdir(tmp_dir):
        file_path = _path.join(tmp_dir, file_name)
        if _path.isfile(file_path) and (_time.time() - _path.getmtime(file_path)) >= 1800:  # 30 min
            _logger.info('Removed temporary file {}'.format(file_path))
            _unlink(file_path)


def _cleanup_sessions():
    session_path = _reg.get('paths.session')
    ttl = int(_reg.get('router.session.ttl', 86400))  # 24 hours
    now = _time.time()

    _logger.info('Cleaning up session data older {} seconds in {}'.format(ttl, session_path))

    for file_name in _listdir(session_path):
        file_path = _path.join(session_path, file_name)
        if _path.isfile(file_path) and (now - _path.getmtime(file_path)) >= ttl:
            _unlink(file_path)
            _logger.info('Removed session file: {}'.format(file_path))

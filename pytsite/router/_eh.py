"""PytSite Router Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import util, reg, logger


def on_cleanup():
    success, failed = util.cleanup_files(reg.get('paths.session'), reg.get('router.session_ttl', 86400))

    for f_path in success:
        logger.debug('Obsolete session file removed: {}'.format(f_path))

    for f_path, e in failed:
        logger.error('Error while removing obsolete session file {}: {}'.format(f_path, e))

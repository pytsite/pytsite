"""PytSite robots.txt Event Handlers.
"""
from os import path
from pytsite import reg as _reg, logger as _logger
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def cron_daily():
    """'pytsite.cron.daily' event handler.
    """
    content = ''
    for user_agent, rules in _api.get_rules().items():
        if rules:
            content += 'User-agent: {}\n'.format(user_agent)
            for rule in rules:
                content += rule + '\n'
            content += '\n'

    out_path = path.join(_reg.get('paths.static'), 'robots.txt')
    with open(out_path, 'w') as f:
        f.write(content)
        _logger.info('File successfully written into {}'.format(out_path))

"""PytSite Plugman Events Handlers
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from . import _api


def update_stage_2():
    for p_name, upd_info in _api.get_update_info().items():
        _api.run_update_hooks(2, p_name, upd_info['version_from'], upd_info['version_to'])
        _api.rm_update_info(p_name)

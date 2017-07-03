"""PytSite Plugman Event Handlers
"""
from pytsite import console as _console
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def setup():
    _console.run_command('plugman:install')


def update_after():
    _api.upgrade()

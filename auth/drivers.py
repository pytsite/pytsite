__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod


class AbstractDriver(ABC):
    def get_login_form(self):
        pass
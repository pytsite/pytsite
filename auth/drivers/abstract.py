"""Abstract auth driver.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from ...core.router import Request, RedirectResponse


class AbstractDriver(ABC):
    @abstractmethod
    def get_login_form(self):
        """Get a login form.
        """
        pass

    @abstractmethod
    def post_login_form(self, args: dict, inp: dict)->RedirectResponse:
        """Post a login form.
        """
        pass
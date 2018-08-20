"""PytSite Routing Errors
"""

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class RuleNotFound(Exception):
    pass


class RuleExists(Exception):
    pass


class RulePathBuildError(Exception):
    pass


class RuleArgumentError(Exception):
    pass

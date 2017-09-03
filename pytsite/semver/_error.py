"""PytSite Semantic Versioning Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class InvalidRequirementString(Exception):
    pass


class InvalidVersionString(Exception):
    pass


class InvalidCondition(Exception):
    pass


class InvalidComparisonOperator(Exception):
    pass

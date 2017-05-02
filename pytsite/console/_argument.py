"""
"""
from typing import Any as _Any
from pytsite import validation as _validation
from . import _option

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Argument(_option.Option):
    @property
    def signature(self) -> str:
        return '<{}>'.format(self._name) if self._required else '[{}]'.format(self._name)


class Choice(Argument):
    def __init__(self, name: str, required: bool = False, default: _Any = None, options: list = None):
        super().__init__(name, required, default)

        if not options:
            raise RuntimeError('Items is not specified')

        rule = _validation.rule.Choice(
            msg_id='pytsite.console@error_argument_choice',
            msg_args={'arg_name': name, 'options': options},
            options=options,
        )

        self._rules.append(rule)
        self._items = options

    @property
    def signature(self) -> str:
        items_str = '|'.join(self._items)

        return '<{}>'.format(items_str) if self._required else '[{}]'.format(items_str)

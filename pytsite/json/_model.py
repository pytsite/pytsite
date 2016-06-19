"""PytSite JSON Support Models.
"""
from typing import Union as _Union, List as _List, Tuple as _Tuple, Dict as _Dict

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class JSONable:
    def jsonable_dict(self, fields: _Union[_List, _Tuple]=(), **kwargs) -> _Dict:
        raise NotImplementedError()

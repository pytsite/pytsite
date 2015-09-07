import re as _re
from werkzeug.wrappers import Request as _Request

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Request(_Request):
    """HTTP request.
    """
    @property
    def values_dict(self) -> dict:
        r = {}

        for part in self.values.lists():
            k = part[0]
            """:type: str"""

            v = part[1]
            """:type: list"""

            list_key = _re.match('([^\[]+)\[\]', k)
            dict_key = _re.match('([^\[]+)\[(\w+)\]', k)

            if list_key:
                k = list_key.group(1)
                r[k] = v
            elif dict_key:
                k = dict_key.group(1)
                sub_k = dict_key.group(2)
                if k not in r:
                    r[k] = {}
                r[k][sub_k] = v if len(v) > 1 else v[0]
            else:
                r[k] = v if len(v) > 1 else v[0]

        return r

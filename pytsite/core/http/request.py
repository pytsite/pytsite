__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from werkzeug.wrappers import Request as Base


class Request(Base):
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

            arr_key = re.match('(\w+)\[\]', k)
            dict_key = re.match('(\w+)\[(\w+)\]', k)

            if arr_key:
                k = arr_key.group(1)
                if k not in r:
                    r[k] = []
                r[k] = v if len(v) > 1 else v[0]
            if dict_key:
                k = dict_key.group(1)
                sub_k = dict_key.group(2)
                if k not in r:
                    r[k] = {}
                r[k][sub_k] = v if len(v) > 1 else v[0]
            else:
                r[k] = v if len(v) > 1 else v[0]

        return r

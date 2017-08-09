import re as _re
from werkzeug.wrappers import Request as _Request
from werkzeug.utils import cached_property as _cached_property

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_dict_list_key_re = _re.compile('([^\[]+)\[(\w+)\]\[\]$')
_dict_key_re = _re.compile('([^\[]+)\[(\w+)\]$')
_list_key_re = _re.compile('([^\[]+)\[\]$')


class Request(_Request):
    """HTTP request.
    """

    @_cached_property
    def inp(self) -> dict:
        r = {}

        for part in self.values.lists():
            k = part[0]  # type: str
            v = part[1]  # type: list

            is_dict_list_key = _dict_list_key_re.match(k)
            is_dict_key = _dict_key_re.match(k)
            is_list_key = _list_key_re.match(k)

            # Key has form 'key[sub_key][]'. Value will be a list inside of a dict.
            if is_dict_list_key:
                k = is_dict_list_key.group(1)
                sub_k = is_dict_list_key.group(2)
                if k not in r:
                    r[k] = {}
                if sub_k not in r[k]:
                    r[k][sub_k] = []

                if len(v) > 1:
                    r[k][sub_k] += v
                else:
                    r[k][sub_k].append(v[0])

            # Key has form 'key[sub_key]'. Value will be a dict.
            elif is_dict_key:
                k = is_dict_key.group(1)
                sub_k = is_dict_key.group(2)
                if k not in r:
                    r[k] = {}
                r[k][sub_k] = v if len(v) > 1 else v[0]

            # Key has form 'key[]'. Value will be a list.
            elif is_list_key:
                k = is_list_key.group(1)
                r[k] = v

            # Key is simple string. Value will be used as-is.
            else:
                # Value always is a list. If list has only one item, extract it.
                if len(v) == 1:
                    v = v[0]

                # Convert some well-known strings to types
                if isinstance(v, str):
                    if v in ('True', 'true'):
                        v = True
                    elif v in ('False', 'false'):
                        v = False
                    elif v in ('None', 'undefined'):
                        v = None

                r[k] = v

        return r

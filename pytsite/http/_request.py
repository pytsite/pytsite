import re as _re
from werkzeug.wrappers import Request as _Request

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Request(_Request):
    """HTTP request.
    """
    @property
    def inp(self) -> dict:
        r = {}

        for part in self.values.lists():
            k = part[0]  # type: str
            v = part[1]  # type: list

            is_list_key = _re.match('([^\[]+)\[\]', k)
            is_dict_key = _re.match('([^\[]+)\[(\w+)\]', k)

            # Key has form 'key[]'. Value will be a list.
            if is_list_key:
                k = is_list_key.group(1)
                r[k] = v

            # Key has form 'key[sub_key]'. Value will be be a dict.
            elif is_dict_key:
                k = is_dict_key.group(1)
                sub_k = is_dict_key.group(2)
                if k not in r:
                    r[k] = {}
                r[k][sub_k] = v if len(v) > 1 else v[0]

            # Key is simple string. Value will be uses as-is.
            else:
                # Value always is a list. If list has only one item, extract it.
                if len(v) == 1:
                    v = v[0]

                # Convert some well-known strings to types
                if isinstance(v, str):
                    if v.isdigit():
                        v = int(v)
                    elif v in ('True', 'true'):
                        v = True
                    elif v in ('False', 'false'):
                        v = False
                    elif v in ('None', 'undefined'):
                        v = None

                r[k] = v

        return r

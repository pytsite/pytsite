__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.wrappers import Request as Base


class Request(Base):
    """HTTP request.
    """

    def get_values_dict(self) -> dict:
        request_values = {}

        for part in self.values.lists():
            print(part)

            k = part[0]
            """:type: str"""

            v = part[1]
            """:type: list"""

            if len(v) > 1:
                request_values[k] = v
            else:
                request_values[k] = v[0]

        return request_values

"""PytSite HTTP Headers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from werkzeug.datastructures import Headers as _Headers


class Headers(_Headers):
    pass

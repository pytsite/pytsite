"""Disqus Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import odm as _odm


class CommentCount(_odm.model.Model):
    def _setup(self):
        self._define_field(_odm.field.String('thread', not_empty=True))
        self._define_field(_odm.field.Integer('count'))

        self._define_index([('thread', _odm.I_ASC)], unique=True)

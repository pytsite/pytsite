"""Disqus Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm as _odm


class CommentCount(_odm.Model):
    def _setup(self):
        self.define_field(_odm.field.String('thread', nonempty=True))
        self.define_field(_odm.field.Integer('count'))

        self.define_index([('thread', _odm.I_ASC)], unique=True)

"""Image model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ..core.odm.fields import *
from ..file.models import File


class Image(File):
    def _setup(self):
        """_setup() hook.
        """
        super()._setup()
        self.define_field(IntegerField('width'))
        self.define_field(IntegerField('height'))
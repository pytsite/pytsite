"""Object Document Mapper.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pymongo import ASCENDING, DESCENDING
from . import models, fields

I_ASC = ASCENDING
I_DESC = DESCENDING

ODMModel = models.ODMModel

"""Object Document Mapper.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pymongo import ASCENDING, DESCENDING, GEO2D
from . import models, fields

I_ASC = ASCENDING
I_DESC = DESCENDING
I_GEO2D = GEO2D

ODMModel = models.ODMModel

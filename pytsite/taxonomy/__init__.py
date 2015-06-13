"""Description.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router, lang
from pytsite.admin import sidebar


lang.register_package(__name__)

router.add_rule('/pytsite/taxonomy/search/<string:model>/<string:query>',
                'pytsite.taxonomy.eps.search_terms')

sidebar.add_section('taxonomy', lang.t(__name__ + '@taxonomy'), 500, ('*',))

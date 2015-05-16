__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ..core import view, metatag, lang


def dashboard(values, request):
    metatag.set_tag('title', lang.t('pytsite.admin@dashboard'))
    return view.render_tpl('pytsite.admin@html')

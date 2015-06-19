"""Currency Plugin Forms
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import form as _form, widget as _widget, lang as _lang, validation as _validation
from . import _functions

class Settings(_form.Base):
    def _setup(self):
        weight = 10
        main_cur = _functions.get_main()
        for cur in _functions.get_currencies(False):
            self.add_widget(_widget.input.Float(
                uid='setting_exchange_rate_' + cur,
                weight=weight,
                label=_lang.t('pytsite.currency@exchange_rate', {'code': cur}),
                h_size='col-xs-12 col-sm-4 col-md-3 col-lg-2',
                value='1.0',
                append=main_cur
            ))
            self.add_rule('setting_exchange_rate_' + cur, _validation.rule.GreaterThan())

            weight += 10

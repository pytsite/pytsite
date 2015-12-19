"""PytSite Currency Models.
"""
from decimal import Decimal as _Decimal
from datetime import datetime as _datetime
from pytsite import odm as _odm, odm_ui as _odm_ui, widget as _widget
from . import _widget as _currency_widget, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Rate(_odm_ui.UIModel):
    """Currency Exchange Rate Model.
    """
    def _setup(self):
        """Hook.
        """
        self._define_field(_odm.field.DateTime('date', nonempty=True))
        self._define_field(_odm.field.String('source', nonempty=True))
        self._define_field(_odm.field.String('destination', nonempty=True))
        self._define_field(_odm.field.Decimal('rate', round=8))

        self._define_index([('date', _odm.I_DESC), ('source', _odm.I_ASC), ('destination', _odm.I_ASC)])

    @property
    def date(self) -> _datetime:
        return self.f_get('date')

    @property
    def source(self) -> str:
        return self.f_get('source')

    @property
    def destination(self) -> str:
        return self.f_get('destination')

    @property
    def rate(self) -> _Decimal:
        return self.f_get('rate')

    @classmethod
    def ui_browser_setup(cls, browser):
        """Setup ODM UI browser hook.

        :type browser: pytsite.odm_ui._browser.Browser
        """
        browser.data_fields = ('date', 'source', 'destination', 'rate')
        browser.default_sort_field = 'date'

    def ui_browser_get_row(self) -> tuple:
        """Get single UI browser row hook.
        """
        return str(self.date), self.source, self.destination, str(self.rate)

    def ui_mass_action_get_entity_description(self):
        return '{}, {} -&gt; {}, {}'.format(str(self.date), self.source, self.destination, str(self.rate))

    def ui_m_form_setup(self, form, stage: str):
        """Modify form setup hook.

        :type form: pytsite.form.Form
        """
        form.add_widget(_widget.select.DateTime(
            uid='date',
            weight=10,
            label=self.t('date'),
            value=self.date if not self.is_new else _datetime.now(),
            h_size='col-sm-4 col-md-3 col-lg-2',
            required=True,
        ))

        form.add_widget(_currency_widget.Select(
            uid='source',
            weight=20,
            label=self.t('source'),
            value=self.source if not self.is_new else _api.get_main(),
            h_size='col-sm-4 col-md-3 col-lg-2',
            required=True,
        ))

        form.add_widget(_currency_widget.Select(
            uid='destination',
            weight=30,
            label=self.t('destination'),
            value=self.destination,
            h_size='col-sm-4 col-md-3 col-lg-2',
            required=True,
        ))

        form.add_widget(_widget.input.Float(
            uid='rate',
            weight=40,
            label=self.t('rate'),
            value=self.rate,
            h_size='col-sm-4 col-md-3 col-lg-2',
            required=True,
            allow_minus=False,
            min=0.01,
        ))

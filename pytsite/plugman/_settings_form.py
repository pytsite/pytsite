"""PytSite Plugin Manager Settings Form.
"""
from pytsite import settings as _settings, widget as _widget, lang as _lang, html as _html
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):

    def _setup_widgets(self):
        self.remove_widget('action-submit')

        table = _widget.static.Table('plugins')

        table.add_row((
            _lang.t('pytsite.plugman@name'),
            _lang.t('pytsite.plugman@description'),
            _lang.t('pytsite.plugman@version'),
            _lang.t('pytsite.plugman@url'),
            _lang.t('pytsite.plugman@actions'),
        ), part='thead')

        for name, plugin in _api.get_plugins().items():
            table.add_row((
                plugin.__name__,
                plugin.__pytsite_plugin_description__,
                plugin.__pytsite_plugin_version__,
                str(_html.A(plugin.__pytsite_plugin_url__, href=plugin.__pytsite_plugin_url__, target='_blank')),
                '',
            ))

        self.add_widget(table)

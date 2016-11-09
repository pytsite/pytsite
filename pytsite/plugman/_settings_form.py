"""PytSite Plugin Manager Settings Form.
"""
from pytsite import settings as _settings, widget as _widget, lang as _lang, html as _html, assetman as _assetman
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(_settings.Form):
    def _setup_form(self, **kwargs):
        super()._setup_form(**kwargs)

        _assetman.add('pytsite.plugman@css/settings-form.css')
        _assetman.add('pytsite.plugman@js/settings-form.js')

    def _setup_widgets(self):
        self.remove_widget('action-submit')

        table = _widget.static.Table('plugins')

        table.add_row((
            _lang.t('pytsite.plugman@description'),
            _lang.t('pytsite.plugman@version'),
            {'content': _lang.t('pytsite.plugman@actions'), 'style': 'width: 1%;'},
        ), part='thead')

        for name, info in sorted(_api.get_info().items()):
            description = str(_html.A(info['description'], href=info['home_url'], target='_blank'))

            actions = ''
            if not info['installed_version']:
                btn = _html.A(cls='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                              href='#', data_name=name, data_ep='plugman/install')
                btn.append(_html.I(cls='fa fa-download'))
                btn.append(_html.Span(_lang.t('pytsite.plugman@install'), cls='text'))
                actions += str(btn)
            else:
                # Upgrade button
                if info['upgradable']:
                    btn = _html.A(cls='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                                  href='#', data_name=name, data_ep='plugman/upgrade')
                    btn.append(_html.I(cls='fa fa-arrow-up'))
                    btn.append(_html.Span(_lang.t('pytsite.plugman@upgrade'), cls='text'))
                    actions += str(btn)

                # Uninstall button
                if not info['required']:
                    btn = _html.A(cls='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                                  href='#', data_name=name, data_ep='plugman/uninstall')
                    btn.append(_html.I(cls='fa fa-trash'))
                    btn.append(_html.Span(_lang.t('pytsite.plugman@uninstall'), cls='text'))
                    actions += str(btn)

            if info['installed_version']:
                version = info['installed_version']
                if info['installed_version'] != info['latest_version'][0]:
                    version += ' ({})'.format(info['latest_version'][0])
            else:
                version = info['latest_version'][0]

            table.add_row((
                description,
                {'content': version, 'cls': 'cell-version'},
                {'content': actions, 'cls': 'cell-actions'},
            ))

        self.add_widget(table)

"""PytSite Plugin Manager Settings Form.
"""
from pytsite import settings as _settings, widget as _widget, lang as _lang, html as _html, assetman as _assetman, \
    reload as _reload, reg as _reg
from . import _api, _error, _plugman_started

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_DEV_MODE = _reg.get('plugman.dev')


class Form(_settings.Form):
    def _setup_form(self, **kwargs):
        """Hook.
        """
        super()._setup_form(**kwargs)

        _assetman.add('pytsite.plugman@css/settings-form.css')
        _assetman.add('pytsite.plugman@js/settings-form.js')

    def _setup_widgets(self):
        """Hook.
        """
        if _DEV_MODE:
            self.add_widget(_widget.static.Text(
                uid='dev_mode_notify',
                title=_lang.t('pytsite.plugman@cannot_manage_plugins_in_dev_mode'),
            ))

            self.remove_widget('action-submit')

            return

        lng = _lang.get_current()
        lic_number = _settings.get('plugman.license')

        lic_input = _widget.input.Text(
            uid='setting_license',
            weight=20,
            label=_lang.t('pytsite.plugman@license'),
            required=True,
        )

        try:
            lic_info = _api.get_license_info()

            lic_input.has_success = True
            if lic_info['expires']:
                lic_input.help = _lang.t('pytsite.plugman@license_expires_at', {'date': lic_info['expires']})

            table = _widget.static.Table(uid='plugins', weight=10)

            # Table header
            table.add_row((
                _lang.t('pytsite.plugman@description'),
                _lang.t('pytsite.plugman@version'),
                {'content': _lang.t('pytsite.plugman@actions'), 'style': 'width: 1%;'},
            ), part='thead')

            for name, info in sorted(_api.get_plugins().items()):
                description = str(_html.Span(info['description'].get(lng)))

                actions = ''
                if not _api.is_installed(name):
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
                    if info['upgradable']:
                        version += ' ({})'.format(info['latest_version'])
                else:
                    version = info['latest_version']

                table.add_row((
                    description,
                    {'content': version, 'cls': 'cell-version'},
                    {'content': actions, 'cls': 'cell-actions'},
                ))

            self.add_widget(table)

        except _error.InvalidLicense:
            if lic_number:
                lic_input.help = _lang.t('pytsite.plugman@invalid_license')
                lic_input.has_error = True

        self.add_widget(lic_input)

        super()._setup_widgets()

    def _on_submit(self):
        if _DEV_MODE:
            return

        try:
            _api.get_license_info()
            if not _plugman_started:
                _reload.reload()
        except _error.InvalidLicense:
            if _plugman_started:
                _reload.reload()

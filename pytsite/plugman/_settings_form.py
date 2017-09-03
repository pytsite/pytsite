"""PytSite Plugin Manager Settings Form.
"""
from pytsite import settings as _settings, widget as _widget, lang as _lang, html as _html, assetman as _assetman, \
    router as _router, semver as _semver
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_DEV_MODE = _router.server_name() == 'local.plugins.pytsite.xyz'


class Form(_settings.Form):
    def _on_setup_form(self, **kwargs):
        """Hook.
        """
        super()._on_setup_form(**kwargs)

        _assetman.preload('pytsite.plugman@css/settings-form.css')
        _assetman.preload('pytsite.plugman@js/settings-form.js')

    def _on_setup_widgets(self):
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
        table = _widget.static.Table(uid='plugins', weight=10)

        # Table header
        table.add_row((
            _lang.t('pytsite.plugman@description'),
            _lang.t('pytsite.plugman@version'),
            {'content': _lang.t('pytsite.plugman@actions'), 'style': 'width: 1%;'},
        ), part='thead')

        for r_plugin_name, p_versions in sorted(_api.remote_plugins_info().items()):
            r_plugin_info = p_versions[_semver.last(p_versions.keys())]
            description = str(_html.Span(r_plugin_info['description'].get(lng)))

            actions = ''

            try:
                l_plugin_info = _api.plugin_info(r_plugin_name)

                version_str = l_plugin_info['version']

                if _semver.compare(l_plugin_info['version'], r_plugin_info['version']) < 0:
                    version_str += ' ({})'.format(r_plugin_info['version'])

                    # Upgrade button
                    btn = _html.A(css='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                                  href='#', data_name=r_plugin_name, data_ep='plugman/upgrade')
                    btn.append(_html.I(css='fa fa-arrow-up'))
                    btn.append(_html.Span(_lang.t('pytsite.plugman@upgrade'), css='text'))
                    actions += str(btn)

                # Uninstall button
                if not _api.get_dependant_plugins(r_plugin_name):
                    btn = _html.A(css='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                                  href='#', data_name=r_plugin_name, data_ep='plugman/uninstall')
                    btn.append(_html.I(css='fa fa-trash'))
                    btn.append(_html.Span(_lang.t('pytsite.plugman@uninstall'), css='text'))
                    actions += str(btn)

            except _error.PluginNotInstalled:
                version_str = r_plugin_info['version']

                # Install button
                btn = _html.A(css='btn btn-xs btn-default action-btn', child_sep='&nbsp;',
                              href='#', data_name=r_plugin_name, data_ep='plugman/install')
                btn.append(_html.I(css='fa fa-download'))
                btn.append(_html.Span(_lang.t('pytsite.plugman@install'), css='text'))
                actions += str(btn)

            table.add_row((
                description,
                {'content': version_str, 'css': 'cell-version'},
                {'content': actions, 'css': 'cell-actions'},
            ))

        self.add_widget(table)

        super()._on_setup_widgets()

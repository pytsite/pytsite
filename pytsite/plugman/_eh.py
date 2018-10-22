"""PytSite Plugman Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console as _console, lang as _lang, package_info as _package_info, events as _events, \
    logger as _logger, semver as _semver, reg as _reg
from . import _api, _error


def on_pytsite_update_stage_2():
    # Update all installed plugins
    _console.print_info(_lang.t('pytsite.plugman@updating_plugins'))
    _console.run_command('plugman:install', {'reload': False})


def on_pytsite_load():
    update_info = _api.get_update_info()

    if not update_info:
        return

    # If there waiting updates exist, reload the application
    if _reg.get('env.type') == 'wsgi':
        _logger.warn('Application needs to be loaded in console to finish plugins update')
        return

    failed_plugins = []

    # Call 'plugin_pre_install()' hooks
    for p_name, info in update_info.items():
        v_to = _semver.Version(info['version_to'])

        try:
            # Check if the plugin is installed and loaded
            plugin = _api.get(p_name)

            # Call plugin_pre_install() hook
            if hasattr(plugin, 'plugin_pre_install') and callable(plugin.plugin_pre_install):
                plugin.plugin_pre_install()
            _events.fire('pytsite.plugman@pre_install', name=p_name, version=v_to)

        except _error.PluginNotLoaded as e:
            _logger.error(e)
            _console.print_warning(_lang.t('pytsite.plugman@plugin_install_error', {
                'plugin': p_name,
                'version': v_to,
                'msg': str(e),
            }))
            failed_plugins.append(p_name)
            continue

    # Finish installing/updating plugins
    for p_name, info in update_info.items():
        if p_name in failed_plugins:
            continue

        plugin = _api.get(p_name)
        v_from = _semver.Version(info['version_from'])
        v_to = _semver.Version(info['version_to'])

        # Call plugin_install() hook
        try:
            _logger.info(_lang.t('pytsite.plugman@installing_plugin', {
                'plugin': p_name,
                'version': v_to,
            }))

            if hasattr(plugin, 'plugin_install') and callable(plugin.plugin_install):
                plugin.plugin_install()
            _events.fire('pytsite.plugman@install', name=p_name, version=v_to)

            _console.print_success(_lang.t('pytsite.plugman@plugin_install_success', {
                'plugin': p_name,
                'version': v_to,
            }))

        except Exception as e:
            _logger.error(e)
            _console.print_warning(_lang.t('pytsite.plugman@plugin_install_error', {
                'plugin': p_name,
                'version': v_to,
                'msg': str(e),
            }))
            continue

        # Update plugin
        if v_from != '0.0.0':
            try:
                _console.print_info(_lang.t('pytsite.plugman@updating_plugin', {
                    'plugin': p_name,
                    'v_from': v_from,
                    'v_to': v_to,
                }))

                # Call plugin_update() hook
                if hasattr(plugin, 'plugin_update') and callable(plugin.plugin_update):
                    plugin.plugin_update(v_from=v_from)
                _events.fire('pytsite.plugman@update', name=p_name, v_from=v_from)

                _console.print_success(_lang.t('pytsite.plugman@plugin_update_success', {
                    'plugin': p_name,
                    'version': v_to,
                }))

            except Exception as e:
                _console.print_warning(_lang.t('pytsite.plugman@plugin_update_error', {
                    'plugin': p_name,
                    'version': v_to,
                    'msg': str(e),
                }))
                continue

        # Remove info from update queue
        _api.rm_update_info(p_name)

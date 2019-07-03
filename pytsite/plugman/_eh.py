"""PytSite Plugman Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import console, lang, events, logger, semver, reg
from . import _api, _error


def on_pytsite_update_stage_2():
    # Update all installed plugins
    console.print_info(lang.t('pytsite.plugman@updating_plugins'))
    console.run_command('plugman:install', {'reload': False})


def on_pytsite_load():
    update_info = _api.get_update_info()

    if not update_info:
        return

    # If there waiting updates exist, reload the application
    if reg.get('env.type') == 'wsgi':
        logger.warn('Application needs to be loaded in console to finish plugins update')
        return

    failed_plugins = []

    # Call 'plugin_pre_install()' hooks
    for p_name, info in update_info.items():
        v_to = semver.Version(info['version_to'])

        try:
            # Check if the plugin is installed and loaded
            plugin = _api.get(p_name)

            # Call plugin_pre_install() hook
            if hasattr(plugin, 'plugin_pre_install') and callable(plugin.plugin_pre_install):
                plugin.plugin_pre_install()

            # Fire 'pre_install' event
            events.fire('pytsite.plugman@pre_install', name=p_name, version=v_to)

        except _error.PluginNotLoaded as e:
            logger.error(e)
            console.print_warning(lang.t('pytsite.plugman@plugin_install_error', {
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
        v_from = semver.Version(info['version_from'])
        v_to = semver.Version(info['version_to'])

        try:
            logger.info(lang.t('pytsite.plugman@installing_plugin', {
                'plugin': p_name,
                'version': v_to,
            }))

            # Call plugin_install() hook
            if hasattr(plugin, 'plugin_install') and callable(plugin.plugin_install):
                plugin.plugin_install()

            # Fire 'install' event
            events.fire('pytsite.plugman@install', name=p_name, version=v_to)

            console.print_success(lang.t('pytsite.plugman@plugin_install_success', {
                'plugin': p_name,
                'version': v_to,
            }))

        except Exception as e:
            logger.error(e)
            console.print_warning(lang.t('pytsite.plugman@plugin_install_error', {
                'plugin': p_name,
                'version': v_to,
                'msg': str(e),
            }))
            continue

        # Update plugin
        if v_from != '0.0.0':
            try:
                console.print_info(lang.t('pytsite.plugman@updating_plugin', {
                    'plugin': p_name,
                    'v_from': v_from,
                    'v_to': v_to,
                }))

                # Call plugin_update() hook
                if hasattr(plugin, 'plugin_update') and callable(plugin.plugin_update):
                    plugin.plugin_update(v_from=v_from)

                # Fire 'update' event
                events.fire('pytsite.plugman@update', name=p_name, v_from=v_from)

                console.print_success(lang.t('pytsite.plugman@plugin_update_success', {
                    'plugin': p_name,
                    'version': v_to,
                }))

            except Exception as e:
                console.print_warning(lang.t('pytsite.plugman@plugin_update_error', {
                    'plugin': p_name,
                    'version': v_to,
                    'msg': str(e),
                }))
                continue

        # Remove info from update queue
        _api.rm_update_info(p_name)

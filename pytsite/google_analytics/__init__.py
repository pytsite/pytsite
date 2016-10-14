"""PytSite Google Analytics Package.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, tpl, permissions, settings, events
    from . import _settings_form, _eh

    lang.register_package(__name__)
    tpl.register_package(__name__)

    permissions.define_permission('google_analytics.settings.manage',
                                  'pytsite.google_analytics@manage_google_analytics_settings', 'app')

    settings.define('google_analytics', _settings_form.Form, 'pytsite.google_analytics@google_analytics',
                    'fa fa-line-chart', 'google_analytics.settings.manage')

    events.listen('pytsite.router.dispatch', _eh.router_dispatch)


_init()

"""Pytsite Disqus Package Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper.
    """
    from pytsite import comments, tpl, lang, events, permissions, settings
    from . import _eh, _comments, _settings_form

    lang.register_package(__name__)
    tpl.register_package(__name__)
    comments.register_driver(_comments.Driver())

    permissions.define_permission('disqus.settings.manage', 'pytsite.disqus@manage_disqus_settings', 'app')
    settings.define('disqus', _settings_form.Form, 'pytsite.disqus@disqus', 'fa fa-comments', 'disqus.settings.manage')

    events.listen('pytsite.update', _eh.pytsite_update)

_init()

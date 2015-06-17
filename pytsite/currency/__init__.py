"""Currency Plugin Package
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite.core import lang
    from pytsite import settings
    from ._form import SettingsForm

    lang.register_package(__name__)

    settings.define_setting('currency', SettingsForm('currency-settings'), __name__ + '@currency', 'fa fa-dollar')

# Package initialization
__init()

# Public API

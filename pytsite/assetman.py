from pytsite.application import Plugin
from pytsite.entity import EntityPlugin


class AssetmanPlugin(Plugin):
    def __init__(self, app):
        app.register_plugin(EntityPlugin(app))

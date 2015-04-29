class Application:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, obj: Plugin)->None:
        self.plugins.append(obj)

    def _init_plugins(self):
        for plugin in self.plugins:
            plugin.init(self)

    def run(self):
        self._init_plugins()

        for plugin in self.plugins:
            plugin.start(self)

class Plugin():
    def init(self, app: Application)->None:
        pass

    def start(self, app: Application)->None:
        pass


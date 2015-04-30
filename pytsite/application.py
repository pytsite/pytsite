import inspect
from os import path
from . import registry


def run():
    sep = str(path.sep)
    root_path = path.dirname(inspect.getouterframes(inspect.currentframe())[1][1])

    registry.set_val('paths.root', root_path)
    registry.set_val('paths.config', root_path + sep + 'config')
    registry.set_val('paths.log', root_path + sep + 'log')
    registry.set_val('paths.tpl', root_path + sep + 'tpl')

    registry.set_driver(registry.FileDriver(registry.get_val('paths.config')))


from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from abc import ABCMeta, abstractmethod

plugins = []


def register_plugin(obj: object):
    plugins.append(obj)


def run():
    for plugin in plugins:
        plugin.init()
        plugin.start()
    pass


class Plugin:
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def start(self):
        pass
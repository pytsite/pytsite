from pytsite.application import Plugin


class EntityPlugin(Plugin):
    def __init__(self, app):
        print('entity init')

    def start(self, app):
        print('entity start')
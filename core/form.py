__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from .widget import Widget


class Form:
    def __init__(self):
        self._legend = None
        self._widgets = []

    def add_widget(self, widget: Widget, weight: int=0):
        self._widgets.append((widget, weight))
        return self

    def fill(self, values: tuple):
        return self

    def render(self)->str:
        pass


def get_form(name: str)->Form:
    pass
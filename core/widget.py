__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from .validation import Rule


class Widget:
    def __init__(self):
        self._value = None
        self._rules = []
        self._children = []

    def add_rule(self, rule: Rule):
        self._rules.append(rule)
        return self

    def validate(self)->bool:
        valid = True
        messages = []
        for rule in self._rules:
            if not rule.validate(self._value):
                messages.append(rule.get_messages())
                valid = False

        return valid

    def add_child(self, widget, weight: int=0):
        self._children.append((widget, 0))
        return self

    def render(self)->str:
        pass

    def get_val(self):
        return self._value
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from abc import ABC, abstractmethod


class Rule(ABC):
    def __init__(self, args: tuple):
        self._messages = dict()
        self._args = args
        self._value = None

    def set_value(self, value):
        self._value = value

    @abstractmethod
    def validate(self, value)->bool:
        pass

    def get_messages(self)->dict:
        return self._messages

    def reset(self):
        self._messages = dict()
        return self
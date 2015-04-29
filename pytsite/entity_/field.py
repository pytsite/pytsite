from bson.dbref import DBRef

class Base:
    _name = None

    _value = None

    def __init__(self, name: str=None, value=None):
        self._name = name
        self.set_value(value)

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value


class String(Base):
    _value = ''

    def set_value(self, value):
        if value is not None and not isinstance(value, str):
            raise Exception('String expected')
        super(String, self).set_value(value)

class List(Base):
    _value = []

    def set_value(self, value):
        if value is not None and not isinstance(value, list):
            raise Exception('List expected')
        super(List, self).set_value(value)

class Ref(Base):
    def set_value(self, value):
        if value is not None and not isinstance(value, DBRef):
            raise Exception('DBRef expected')
        super(Ref, self).set_value(value)
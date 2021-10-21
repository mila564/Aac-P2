class Register:
    def __init__(self, name, value):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.__value = val

    def __eq__(self, other):
        if isinstance(other, Register):
            return self.__name == other.__name
        else:
            return False

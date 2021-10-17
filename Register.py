class Register:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_name(self):
        return self.name

    def get_value(self):
        return self.name

    def set_value(self, value):
        try:
            self.value = int(value)
        except TypeError:
            print("Invalid type")

    def __eq__(self, other):
        if isinstance(other, Register):
            return self.name == other.name
        return False

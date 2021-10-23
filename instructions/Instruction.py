import abc


class Instruction:
    def __init__(self, op_code):
        self.__op_code = op_code

    @property
    def op_code(self):
        return self.__op_code

    @abc.abstractmethod
    def __str__(self):
        pass



class PipelineRegister:
    def __init__(self, instruction):
        self.__instruction = instruction

    @property
    def instruction(self):
        return self.__instruction

    @instruction.setter
    def instruction(self, i):
        self.__instruction = i

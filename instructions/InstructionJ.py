from instructions.Instruction import Instruction


class InstructionJ(Instruction):
    def __init__(self, op_code, target):
        super().__init__(op_code)
        self.__target = target

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, t):
        self.__target = t

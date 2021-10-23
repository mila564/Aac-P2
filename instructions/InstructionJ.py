from abc import ABC

from instructions.Instruction import Instruction


class InstructionJ(Instruction, ABC):
    def __init__(self, op_code, target):
        super().__init__(op_code)
        self.__target = target

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, t):
        self.__target = t

    def __str__(self):
        return str(self.op_code) + " " + str(self.target)

from abc import ABC

from instructions.Instruction import Instruction


class InstructionR(Instruction, ABC):
    def __init__(self, op_code, rd, rs, rt):
        super().__init__(op_code)
        self.__rd = rd
        self.__rs = rs
        self.__rt = rt

    @property
    def rd(self):
        return self.__rd

    @property
    def rs(self):
        return self.__rs

    @property
    def rt(self):
        return self.__rt

    @rd.setter
    def rd(self, reg_rd):
        self.__rd = reg_rd

    @rs.setter
    def rs(self, reg_rs):
        self.__rs = reg_rs

    @rt.setter
    def rt(self, reg_rt):
        self.__rt = reg_rt

    def __str__(self):
        return str(self.op_code) + " " + str(self.__rd.name) + ", " + str(self.__rs.name) + ", " + str(self.__rt.name)

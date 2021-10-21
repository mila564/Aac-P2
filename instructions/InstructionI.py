from instructions.Instruction import Instruction


class InstructionI(Instruction):
    def __init__(self, op_code, rt, offset, rs):
        super().__init__(op_code)
        self.__rt = rt
        self.__offset = offset
        self.__rs = rs

    @property
    def rt(self):
        return self.__rt

    @property
    def offset(self):
        return self.__offset

    @property
    def rs(self):
        return self.__rs

    @rt.setter
    def rt(self, reg_rt):
        self.__rt = reg_rt

    @offset.setter
    def offset(self, o):
        self.__offset = o

    @rs.setter
    def rs(self, reg_rs):
        self.__rs = reg_rs

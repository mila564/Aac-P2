from instructions.Instruction import Instruction
from RegisterFile import Register


class InstructionR(Instruction):
    def __init__(self, cop, rd, rs, rt):
        super().__init__(cop)
        try:
            self.rd = Register(rd)
            self.rs = Register(rs)
            self.rt = Register(rt)
        except TypeError:
            print("The type of some operand is not correct")

    def get_rd(self):
        return self.rd

    def get_rs(self):
        return self.rs

    def get_rt(self):
        return self.rt

    def set_rd(self, rd):
        try:
            self.rd = Register(rd)
        except TypeError:
            print("Invalid type")

    def set_rt(self, rt):
        try:
            self.rs = Register(rt)
        except TypeError:
            print("Invalid type")

    def set_rs(self, rs):
        try:
            self.rs = Register(rs)
        except TypeError:
            print("Invalid type")

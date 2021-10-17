from RegisterFile import Register
from instructions.Instruction import Instruction


class InstructionI(Instruction):
    def __init__(self, cop, rt, offset, rs):
        super().__init__(cop)
        try:
            self.rt = Register(rt)
            self.offset = int(offset)
            self.rs = Register(rs)
        except TypeError:
            print("The type of some operand is not correct")

    def get_rt(self):
        return self.rt

    def get_offset(self):
        return self.offset

    def get_rs(self):
        return self.rs

    def set_rt(self, rt):
        try:
            self.rs = Register(rt)
        except TypeError:
            print("Invalid type")

    def set_offset(self, offset):
        try:
            self.offset = int(offset)
        except TypeError:
            print("Invalid type")

    def set_rs(self, rs):
        try:
            self.rs = Register(rs)
        except TypeError:
            print("Invalid type")

from RegisterFile import Register
class ArithmeticLogicUnit:
    def __init__(self, reg1, reg2):
        try:
            self.op1 = Register(reg1)
            self.op2 = Register(reg2)
        except TypeError:
            pass

    def beq(self):
        return self.op1.getValue() == self.op2.getValue()

    def add(self):
        return self.op1.getValue() + self.op2.getValue()

    def sub(self):
        return self.op1.getValue() - self.op2.getValue()

    def mul(self):
        return self.op1.getValue() * self.op2.getValue()

    def rem(self):
        return self.op1.getValue() % self.op2.getValue()

    def bnez(self):
        return self.op1.getValue() != 0



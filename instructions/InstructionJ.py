from instructions.Instruction import Instruction


class InstructionJ(Instruction):
    def __init__(self, cop, target):
        super().__init__(cop)
        try:
            self.target = int(target)
        except TypeError:
            print("The type of the operand is not correct")

    def get_target(self):
        return self.target

    def set_target(self, target):
        try:
            self.target = int(target)
        except TypeError:
            print("Invalid type")

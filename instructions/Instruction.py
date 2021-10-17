class Instruction:
    def __init__(self, op_code):
        try:
            self.opCode = str(op_code)
        except TypeError:
            print("The operation code is not a string")

    def get_op_code(self):
        return self.opCode

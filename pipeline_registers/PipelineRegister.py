from instructions.Instruction import Instruction


class PipelineRegister:
    def __init__(self, instruction):
        try:
            self.instruction = Instruction(instruction)
        except TypeError:
            print("Invalid type")

    def get_instruction(self):
        return self.instruction

    def set_instruction(self, instruction):
        try:
            self.instruction = Instruction(instruction)
        except TypeError:
            print("Invalid type")

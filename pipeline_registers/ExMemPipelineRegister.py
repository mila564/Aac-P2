from pipeline_registers.PipelineRegister import PipelineRegister


class ExMemPipelineRegister(PipelineRegister):
    def __init__(self, instruction, value):
        super().__init__(instruction)
        try:
            self.value = int(value)
        except TypeError:
            print("Invalid type")

    def get_value(self):
        return self.value

    def set_value(self, value):
        try:
            self.value = int(value)
        except TypeError:
            print("Invalid type")

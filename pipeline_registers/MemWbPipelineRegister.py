from pipeline_registers.PipelineRegister import PipelineRegister


class MemWbPipelineRegister(PipelineRegister):
    def __init__(self, instruction):
        super().__init__(instruction)

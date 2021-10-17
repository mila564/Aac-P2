from pipeline_registers.PipelineRegister import PipelineRegister


class IfIdPipelineRegister(PipelineRegister):
    def __init__(self, instruction):
        super().__init__(instruction)

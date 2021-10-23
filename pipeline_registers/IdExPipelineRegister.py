from abc import ABC

from pipeline_registers.PipelineRegister import PipelineRegister


class IdExPipelineRegister(PipelineRegister, ABC):

    def __str__(self):
        return str("ID/EX [Instruction] => ") + str(self.instruction)

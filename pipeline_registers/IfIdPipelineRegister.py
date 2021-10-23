from abc import ABC

from pipeline_registers.PipelineRegister import PipelineRegister


class IfIdPipelineRegister(PipelineRegister, ABC):

    def __str__(self):
        return str("IF/ID [Instruction] => ") + str(self.instruction)

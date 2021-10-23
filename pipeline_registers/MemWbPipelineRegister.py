from abc import ABC

from pipeline_registers.PipelineRegister import PipelineRegister


class MemWbPipelineRegister(PipelineRegister, ABC):

    def __str__(self):
        return str("MEM/WB [Instruction] => ") + str(self.instruction)

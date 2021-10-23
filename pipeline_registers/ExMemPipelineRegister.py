from abc import ABC

from pipeline_registers.PipelineRegister import PipelineRegister


class ExMemPipelineRegister(PipelineRegister, ABC):
    def __init__(self, instruction, val):
        super().__init__(instruction)
        self.__val = val

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, v):
        self.__val = v

    def __str__(self):
        return str("EX/MEM [Instruction / ALU result] => ") + str(self.instruction) + " - " + str(self.__val)

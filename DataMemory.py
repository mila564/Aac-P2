import copy

from instructions.InstructionI import InstructionI
from pipeline_registers.ExMemPipelineRegister import ExMemPipelineRegister
from pipeline_registers.MemWbPipelineRegister import MemWbPipelineRegister


class DataMemory:
    def __init__(self):
        self.data = []
        for i in range(58):
            self.data.append(0)

    def print_data_memory_state(self):
        print("Data Memory: ")
        for i in range(58):
            print("Index " + str(i) + ": " + str(self.data[i]))

    def memory(self, ex_mem):
        try:
            ex_mem = ExMemPipelineRegister(ex_mem)
            mem_wb = MemWbPipelineRegister()
            instruction = ex_mem.get_instruction()
            operation_code = instruction.get_op_code()
            if operation_code == "lw" or operation_code == "sw":
                instruction = InstructionI(instruction)
                instruction_mem_wb = copy.deepcopy(instruction)
                rt = instruction_mem_wb.get_rt()
                if operation_code == "lw":
                    rt.set_value(self.data[ex_mem.get_value()])
                else:  # sw
                    self.data[ex_mem.get_value()] = rt.get_value()
                mem_wb.set_instruction(instruction_mem_wb)
                return mem_wb
            else:
                return None  # a J/R instruction doesn't go through this phase
        except TypeError:
            print("Invalid type")

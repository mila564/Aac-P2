import copy

from pipeline_registers.MemWbPipelineRegister import MemWbPipelineRegister


class DataMemory:
    def __init__(self):
        self.data = []
        for i in range(58):
            self.data.append(0)
        self.data[4] = 3
        self.data[5] = 2

    def data_memory_size(self):
        return len(self.data)

    def __str__(self):
        s = "Data memory [Index: value] => "
        for i in range(58):
            s += "[" + str(i) + ": " + str(self.data[i]) + "]"
        return s

    def memory(self, ex_mem):
        if ex_mem is None:
            return None
        else:
            instruction_ex = ex_mem.instruction
            operation_code = instruction_ex.op_code
            instruction_mem_wb = copy.deepcopy(instruction_ex)
            if operation_code == "lw" or operation_code == "sw":
                if operation_code == "lw":
                    instruction_mem_wb.rt.value = self.data[ex_mem.val % self.data_memory_size()]
                else:
                    self.data[ex_mem.val % self.data_memory_size()] = instruction_mem_wb.rt.value
            return MemWbPipelineRegister(instruction_mem_wb)

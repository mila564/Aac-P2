import copy

from pipeline_registers.MemWbPipelineRegister import MemWbPipelineRegister


class DataMemory:
    def __init__(self):
        self.data = []
        for i in range(58):
            self.data.append(0)
        self.data[4] = 3  # We suppose a = 3
        self.data[5] = 2  # b = 2

    def data_memory_size(self):
        return len(self.data)

    def print_data_memory_state(self):
        print("---------------------")
        print("Data Memory: ")
        for i in range(58):  # 58 integer positions => 232 positions of 1 byte in mips memory
            print("Index " + str(i) + ": " + str(self.data[i]))
        print("---------------------")

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
                else:  # sw
                    self.data[ex_mem.val % self.data_memory_size()] = instruction_mem_wb.rt.value
                    # module because of lw/sw result (if it's bigger that memory's capacity)
            return MemWbPipelineRegister(instruction_mem_wb)

from Register import Register

from instructions.InstructionI import InstructionI
from instructions.InstructionJ import InstructionJ
from instructions.InstructionR import InstructionR

from pipeline_registers.IdExPipelineRegister import IdExPipelineRegister


class RegisterFile:
    def __init__(self):
        register_names = ["$zero", "$at", "$v0", "$v1", "$a0", "$a1",
                          "$a2", "$a3", "$t0", "$t1", "$t2", "$t3",
                          "$t4", "$t5", "$t6", "$t7", "$s0", "$s1",
                          "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
                          "$t8", "$t9", "$k0", "$k1", "$gp", "$sp",
                          "$fp", "$ra"]
        self.register_file = []
        self.positions = {}
        for i in range(32):
            self.register_file.append(Register(register_names[i], 0))
            self.positions[register_names[i]] = i
        index_reg = self.positions["$t0"]
        self.register_file[index_reg].value = 4

    def __str__(self):
        s = "Register file [Name: value] => "
        for i in range(32):
            s += "[" + str(self.register_file[i]) + "]"
        return s

    def instruction_decode(self, if_id, instruction_execution, instruction_mem, effective_jump):
        if if_id is None:
            return None
        elif effective_jump:
            return None
        else:
            instruction_fetch = if_id.instruction
            if isinstance(instruction_fetch, InstructionI):
                index_rt = self.positions[instruction_fetch.rt.name]
                index_rs = self.positions[instruction_fetch.rs.name]
                rt = Register(self.register_file[index_rt].name,
                              self.register_file[index_rt].value)
                rs = Register(self.register_file[index_rs].name,
                              self.register_file[index_rs].value)
                instruction_decode = InstructionI(instruction_fetch.op_code, rt, instruction_fetch.offset, rs)
            elif isinstance(instruction_fetch, InstructionR):
                index_rd = self.positions[instruction_fetch.rd.name]
                index_rt = self.positions[instruction_fetch.rt.name]
                index_rs = self.positions[instruction_fetch.rs.name]
                rd = Register(self.register_file[index_rd].name,
                              self.register_file[index_rd].value)
                rt = Register(self.register_file[index_rt].name,
                              self.register_file[index_rt].value)
                rs = Register(self.register_file[index_rs].name,
                              self.register_file[index_rs].value)
                instruction_decode = InstructionR(instruction_fetch.op_code, rd, rs, rt)
            elif isinstance(instruction_fetch, InstructionJ):
                instruction_decode = InstructionJ(instruction_fetch.op_code, instruction_fetch.target)
            if isinstance(instruction_decode, InstructionI) or isinstance(instruction_decode, InstructionR):
                if instruction_execution is not None:
                    if isinstance(instruction_execution, InstructionR):
                        if instruction_execution.rd.__eq__(instruction_decode.rs):
                            instruction_decode.rs.value = instruction_execution.rd.value
                        elif instruction_execution.rd.__eq__(instruction_decode.rt):
                            instruction_decode.rt.value = instruction_execution.rd.value
                    elif instruction_execution.op_code in ["addi", "subi"]:  # Revise condition
                        if instruction_execution.rt.__eq__(instruction_decode.rs):
                            instruction_decode.rs.value = instruction_execution.rt.value
                        elif instruction_execution.rt.__eq__(instruction_decode.rt):
                            instruction_decode.rt.value = instruction_execution.rt.value
                    if instruction_execution.op_code == "lw" and (instruction_execution.rt.__eq__(instruction_decode.rs)
                                                               or instruction_execution.rt.__eq__(instruction_decode.rt)):
                        return None, True
                if instruction_mem is not None and instruction_mem.op_code == "lw":
                    if instruction_mem.rt.__eq__(instruction_decode.rs):
                        instruction_decode.rs.value = instruction_mem.rt.value
                    elif instruction_mem.rt.__eq__(instruction_decode.rt):
                        instruction_decode.rt.value = instruction_mem.rt.value
            return IdExPipelineRegister(instruction_decode), False

    def write_back(self, mem_wb):
        if mem_wb is not None:
            instruction_mem_wb = mem_wb.instruction
            operation_code = instruction_mem_wb.op_code
            index = 0
            if operation_code in ["lw", "addi", "subi"]:
                rt = instruction_mem_wb.rt
                index = self.positions[rt.name]
                self.register_file[index].value = rt.value
            elif operation_code in ["add", "sub", "mul", "rem"]:
                rd = instruction_mem_wb.rd
                index = self.positions[rd.name]
                self.register_file[index].value = rd.value

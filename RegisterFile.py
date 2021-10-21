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
        # We suppose that la $t0, a where 4 is a's memory address
        index_reg = self.positions["$t0"]  # index_reg = 8
        self.register_file[index_reg].value = 4  # $t0 = 4

    def print_register_file_state(self):
        print("Register File: ")
        print("Name|Value")
        for i in range(32):
            print(self.register_file[i].name + "|" + str(self.register_file[i].value))

    def instruction_decode(self, if_id, ex_mem, mem_wb, effective_jump, insert_bubble):
        if if_id is None:
            return None
        elif effective_jump:
            return None  # We need to erase the instruction followed by j/beq
        else:
            instruction_fetch = if_id.instruction
            if isinstance(instruction_fetch, InstructionI):
                # sw/lw rt, offset(rs)
                # addi/subi rt, rs, offset
                # beq rt, rs, offset
                index_rt = self.positions[instruction_fetch.rt.name]
                index_rs = self.positions[instruction_fetch.rs.name]
                rt = Register(self.register_file[index_rt].name,
                              self.register_file[index_rt].value)
                rs = Register(self.register_file[index_rs].name,
                              self.register_file[index_rs].value)
                instruction_decode = InstructionI(instruction_fetch.op_code, rt, instruction_fetch.offset, rs)
            elif isinstance(instruction_fetch, InstructionR):
                # mul rd, rs, rt
                index_rd = self.positions[instruction_fetch.rd.name]
                index_rt = self.positions[instruction_fetch.rt.name]
                index_rs = self.positions[instruction_fetch.rs.name]
                rd = Register(self.register_file[index_rd].name,
                              self.register_file[index_rd].value)
                rt = Register(self.register_file[index_rt].name,
                              self.register_file[index_rt].value)
                rs = Register(self.register_file[index_rs].name,
                              self.register_file[index_rs].value)
                instruction_decode = InstructionR(instruction_fetch.op_code, rd, rt, rs)
            elif isinstance(instruction_fetch, InstructionJ):
                instruction_decode = InstructionJ(instruction_fetch.op_code, instruction_fetch.target)
            if isinstance(instruction_decode, InstructionI) or isinstance(instruction_decode, InstructionR):
                # Execution forwarding
                if isinstance(ex_mem.instruction, InstructionR):
                    if ex_mem.instruction.rd__eq__(instruction_decode.rs):
                        instruction_decode.rs.value = ex_mem.instruction.rd.value
                    elif ex_mem.instruction.rd__eq__(instruction_decode.rt):
                        instruction_decode.rt.value = ex_mem.instruction.rd.value
                elif ex_mem.instruction.op_code in ["addi", "subi"]: # Revise condition
                    if ex_mem.instruction.rt__eq__(instruction_decode.rs):
                        instruction_decode.rs.value = ex_mem.instruction.rd.value
                    elif ex_mem.instruction.rt__eq__(instruction_decode.rt):
                        instruction_decode.rt.value = ex_mem.instruction.rd.value
                # Insert bubble
                if ex_mem.instruction.op_code == "lw":
                    insert_bubble = True
                # Memory forwarding
                if mem_wb.instruction.op_code == "lw":
                    if mem_wb.instruction.rt__eq__(instruction_decode.rs):
                        instruction_decode.rs.value = mem_wb.instruction.rt.value
                    elif mem_wb.instruction.rt__eq__(instruction_decode.rt):
                        instruction_decode.rt.value = mem_wb.instruction.rt.value
            return IdExPipelineRegister(instruction_decode)

    def write_back(self, mem_wb):
        if mem_wb is None:
            return None
        else:
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
            else:  # Sw, beq or j instructions don't go through this phase
                return None

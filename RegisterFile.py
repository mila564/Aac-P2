from Register import Register
from instructions.Instruction import Instruction
from instructions.InstructionI import InstructionI
from instructions.InstructionJ import InstructionJ
from instructions.InstructionR import InstructionR
from pipeline_registers.IdExPipelineRegister import IdExPipelineRegister
from pipeline_registers.IfIdPipelineRegister import IfIdPipelineRegister
from pipeline_registers.MemWbPipelineRegister import MemWbPipelineRegister


class RegisterFile:
    def __init__(self):
        register_names = ["$zero", "$at", "$v0", "$v1", "$a0", "$a1",
                          "$a2", "$a3", "$t0", "$t1", "$t2", "$t3",
                          "$t4", "$t5", "$t6", "$t7", "$s0", "$s1",
                          "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
                          "$t8", "$t9", "$k0", "$k1", "$gp", "$sp",
                          "$fp", "$ra"]
        self.registerFile = []
        self.positions = {}
        for i in range(32):
            self.registerFile.append(Register(register_names[i], 0))
            self.positions[register_names[i]] = i

    def print_register_file_state(self):
        print("Register File: ")
        print("Name|Value")
        for i in range(32):
            print(self.registerFile[i].get_name() + "|" + self.registerFile[i].get_value())

    def instruction_decode(self, if_id):
        try:
            if_id = IfIdPipelineRegister(if_id)
            instruction_fetch = if_id.get_instruction()
            instruction_decode = Instruction(instruction_fetch.get_op_code())
            if instruction_fetch.isinstance(InstructionI):
                instruction_fetch = InstructionI(instruction_fetch)
                # sw/lw rt, offset(rs)
                # addi/subi rt, rs, offset
                # beq rt, rs, offset
                index_rt = self.positions[instruction_fetch.rt.get_name()]
                index_rs = self.positions[instruction_fetch.rs.get_name()]
                rt = Register(self.registerFile[index_rt].get_name(),
                              self.registerFile[index_rt].get_value())
                rs = Register(self.registerFile[index_rs].get_name(),
                              self.registerFile[index_rs].get_value())
                instruction_decode = InstructionI(instruction_decode)
                instruction_decode.set_rt(rt)
                instruction_decode.set_offset(instruction_fetch.get_offset())
                instruction_decode.set_rs(rs)
            elif instruction_fetch.isinstance(InstructionR):
                # mul rd, rs, rt
                instruction_fetch = InstructionR(instruction_fetch)
                index_rd = self.positions[instruction_fetch.rd.get_name()]
                index_rt = self.positions[instruction_fetch.rt.get_name()]
                index_rs = self.positions[instruction_fetch.rs.get_name()]
                rd = Register(self.registerFile[index_rd].get_name(),
                              self.registerFile[index_rd].get_value())
                rt = Register(self.registerFile[index_rt].get_name(),
                              self.registerFile[index_rt].get_value())
                rs = Register(self.registerFile[index_rs].get_name(),
                              self.registerFile[index_rs].get_value())
                instruction_decode = InstructionR(instruction_decode)
                instruction_decode.set_rd(rd)
                instruction_decode.set_rt(rt)
                instruction_decode.set_rs(rs)
            elif instruction_fetch.isinstance(InstructionJ):
                instruction_fetch = InstructionJ(instruction_fetch)
                instruction_decode = InstructionJ(instruction_decode)
                instruction_decode.set_target(instruction_fetch.get_target())
            else:
                raise ValueError
            return IdExPipelineRegister(instruction_decode)
        except TypeError:
            print("Invalid type")

    def write_back(self, mem_wb):
        try:
            mem_wb = MemWbPipelineRegister(mem_wb)
            instruction = mem_wb.get_instruction()
            operation_code = instruction.get_op_code()
            if operation_code == "lw":
                instruction = InstructionI(instruction)
                rt = instruction.get_rt()
                self.positions[rt.get_name()] = rt.get_value()
            elif operation_code in ["add", "sub", "mul", "rem"]:
                instruction = InstructionR(instruction)
                rd = instruction.get_rd()
                self.positions[rd.get_name()] = rd.get_value()
            else:   # sw, beq or j instruction don't go through this phase
                return None
        except RuntimeError:  # we got None at the entry
            return None

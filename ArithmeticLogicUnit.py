import copy

from ProgramCounter import ProgramCounter
from RegisterFile import Register
from instructions.InstructionI import InstructionI
from instructions.InstructionR import InstructionR
from pipeline_registers.ExMemPipelineRegister import ExMemPipelineRegister
from pipeline_registers.IdExPipelineRegister import IdExPipelineRegister


class ArithmeticLogicUnit:
    @staticmethod
    def reg_op(rs, rt, op):
        op1 = Register(rs)
        op2 = Register(rt)
        op3 = str(op)
        if op3 == "+":
            return op1.get_value() + op2.get_value()
        elif op3 == "==":
            return op1.get_value() == op2.get_value()
        elif op3 == "-":
            return op1.get_value() - op2.get_value()
        else:
            return op1.get_value() % op2.get_value()

    @staticmethod
    def immediate_op(rs, offset, op):
        op1 = Register(rs)
        op2 = int(offset)
        op3 = str(op)
        if op3 == "+":
            return op1.get_value() + op2
        else:
            return op1.get_value() - op2

    def add(self, rs, rt):
        self.reg_op(rs, rt, "+")

    def sub(self, rs, rt):
        self.reg_op(rs, rt, "-")

    def addi(self, rs, offset):
        self.immediate_op(rs, offset, "+")

    def subi(self, rs, offset):
        self.immediate_op(rs, offset, "-")

    def rem(self, rs, rt):
        self.reg_op(rs, rt, "%")

    def beq(self, rs, rt):
        self.reg_op(rs, rt, "==")

    def mem_op(self, rs, offset):
        self.immediate_op(rs, offset, "+")

    def execution(self, id_ex, pc):
        id_ex = IdExPipelineRegister(id_ex)
        ex_mem = ExMemPipelineRegister()
        instruction_decode = id_ex.get_instruction()
        operation_code = instruction_decode.get_op_code()
        if operation_code in ["add", "sub", "mul", "rem"]:
            instruction_decode = InstructionR(instruction_decode)
            instruction_ex = copy.deepcopy(instruction_decode)
            rd = instruction_ex.get_rd()
            if operation_code == "add":
                rd.set_value(self.add(instruction_ex.get_rs(), instruction_ex.get_rt()))
            elif operation_code == "sub":
                rd.set_value(self.sub(instruction_ex.get_rs(), instruction_ex.get_rt()))
            elif operation_code == "mul":
                rd.set_value(self.mul(instruction_ex.get_rs(), instruction_ex.get_rt()))
            else:
                rd.set_value(self.rem(instruction_ex.get_rs(), instruction_ex.get_rt()))
        elif operation_code in ["beq", "addi", "subi", "lw", "sw"]:
            instruction_decode = InstructionI(instruction_decode)
            instruction_ex = copy.deepcopy(instruction_decode)
            if operation_code == "beq":
                try:
                    pc = ProgramCounter(pc)
                except TypeError:
                    print("Invalid type")
                if self.beq(instruction_ex.get_rt(), instruction_ex.get_rs()):
                    pc.set_address(instruction_ex.get_offset())
            elif operation_code == "lw" or operation_code == "sw":
                ex_mem.set_value(self.mem_op(instruction_ex.get_rs(),
                                             instruction_ex.get_offset()))
            else:
                rt = instruction_ex.get_rt()
                if operation_code == "addi":
                    rt.set_value(self.addi(instruction_ex.get_rs(),
                                           instruction_ex.get_offset()))
                else:  # subi
                    rt.set_value(self.subi(instruction_ex.get_rs(),
                                           instruction_ex.get_offset()))
        else:
            return None  # a J instruction doesn't go through this phase
        ex_mem.set_instruction(instruction_ex)
        return ex_mem

import copy

from pipeline_registers.ExMemPipelineRegister import ExMemPipelineRegister


class ArithmeticLogicUnit:
    @staticmethod
    def reg_op(rs, rt, op):
        if op == "+":
            return rs.value + rt.value
        elif op == "==":
            return rs.value == rt.value
        elif op == "-":
            return rs.value - rt.value
        else:
            return rs.value % rt.value

    @staticmethod
    def immediate_op(rs, offset, op, divider):  # Add divider parameter because of lw/sw instructions
        if op == "+":
            res = rs.value + int(offset / divider)
            return res
        else:
            return rs.value - offset / divider

    def add(self, rs, rt):
        return self.reg_op(rs, rt, "+")

    def sub(self, rs, rt):
        return self.reg_op(rs, rt, "-")

    def addi(self, rs, offset):
        return self.immediate_op(rs, offset, "+", 1)

    def subi(self, rs, offset):
        return self.immediate_op(rs, offset, "-", 1)

    def rem(self, rs, rt):
        return self.reg_op(rs, rt, "%")

    def beq(self, rs, rt):
        return self.reg_op(rs, rt, "==")

    def mem_op(self, rs, offset):
        return self.immediate_op(rs, offset, "+", 4)

    def execution(self, id_ex, pc, effective_jump):
        if id_ex is None:
            return None
        else:
            instruction_decode = id_ex.instruction
            operation_code = instruction_decode.op_code
            instruction_ex = copy.deepcopy(instruction_decode)
            value = None
            if operation_code in ["add", "sub", "mul", "rem"]:
                if operation_code == "add":
                    instruction_ex.rd.value = self.add(instruction_ex.rs, instruction_ex.rt)
                elif operation_code == "sub":
                    instruction_ex.rd.value = self.sub(instruction_ex.rs, instruction_ex.rt)
                elif operation_code == "mul":
                    instruction_ex.rd.value = self.mul(instruction_ex.rs, instruction_ex.rt)
                else:
                    instruction_ex.rd.value = self.rem(instruction_ex.rs, instruction_ex.rt)
            elif operation_code in ["beq", "addi", "subi", "lw", "sw"]:
                if operation_code == "beq":
                    if self.beq(instruction_ex.rt, instruction_ex.rs):
                        pc.address = instruction_ex.offset
                        effective_jump = True
                elif operation_code == "lw" or operation_code == "sw":
                    value = self.mem_op(instruction_ex.rs, instruction_ex.offset)
                else:
                    if operation_code == "addi":
                        instruction_ex.rt.value = self.addi(instruction_ex.rs, instruction_ex.offset)
                    else:  # subi
                        instruction_ex.rt.value = self.subi(instruction_ex.rs, instruction_ex.offset)
            elif operation_code == "j":
                pc.address = instruction_ex.target  # We change pc to fetch the instruction addressed by target
                effective_jump = True
            return ExMemPipelineRegister(instruction_ex, value)

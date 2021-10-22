import os
import re

from RegisterFile import Register

from instructions.InstructionI import InstructionI
from instructions.InstructionJ import InstructionJ
from instructions.InstructionR import InstructionR

from pipeline_registers.IfIdPipelineRegister import IfIdPipelineRegister


class InstructionMemory:
    def __init__(self):
        self.instructions = []
        self.labels = {}
        with open(os.getcwd() + '/instructions.txt') as f:
            for linea in f:
                self.instructions.append(linea)
        self.place_labels()

    def print_instruction_memory_state(self):
        print("Instruction Memory: ")
        for i in self.instructions:
            print(i)

    def print_labels_dic(self):
        print("Labels: ")
        for k, v in self.labels.items():
            print(k, v)

    def get_last_instruction_address(self):
        return len(self.instructions) - 1

    def place_labels(self):
        for i in range(len(self.instructions)):
            instruction_string = self.instructions[i]
            instruction_array_string = instruction_string.split(" ")
            if not (instruction_array_string[0] in ["lw", "sw", "addi", "subi",
                                                    "beq", "add", "sub", "rem", "mul", "j"]):
                label = instruction_array_string[0]  # This is a label
                label = re.sub(":", "", label)  # We remove last :
                self.labels[label] = i

    def instruction_fetch(self, pc, insert_bubble, if_id):
        if pc.address > self.get_last_instruction_address():
            return None  # There's any instruction to fetch
        elif insert_bubble:  # If there's a bubble, then this instruction must repeat decode phase
            return if_id
        instruction_array_fetch = str(self.instructions[pc.address]).split()  # addi $t1, $zero, 1 => ['addi',
        # '$t1,', '$zero,', '1']
        instruction_fetch = self.create_instruction_for_if_id_register(instruction_array_fetch, pc.address)
        return IfIdPipelineRegister(instruction_fetch)

    def create_instruction_for_if_id_register(self, instruction_array_fetch, pc_address):
        operation_code = instruction_array_fetch[0]
        # We use split method
        # lw $s0, 0($t0) => ['lw', '$s0,', '0($t0)']
        # beq $t3, $zero, Fin => ['beq', '$t3,', '$zero,', 'Fin']
        # addi $t1, $zero, 1 => ['addi', '$t1,', '$zero,', '1']
        if operation_code in ["lw", "sw", "beq", "addi", "subi"]:  # Type I
            rt_name_register = re.sub(",", "", instruction_array_fetch[1])  # We remove extra comma in rt
            if operation_code in ["lw", "sw"]:
                offset_register = instruction_array_fetch[2]  # offset_register ='0($t0)'
                offset_register = offset_register.split("(")  # offset_register = ['0', '$t0)']
                offset = int(offset_register[0])  # offset = 0
                rs_name_register = offset_register[1]  # rs_name_register = '$t0)'
                rs_name_register = re.sub("\\)", "", rs_name_register)  # rs_name_register = '$t0'
            elif operation_code == "beq":
                rs_name_register = re.sub(",", "", instruction_array_fetch[2])  # We remove extra commas in rs
                offset = self.labels[instruction_array_fetch[3]]  # We get memory address
            else:  # addi o subi
                rs_name_register = re.sub(",", "", instruction_array_fetch[2])  # We remove extra commas in rs
                offset = int(instruction_array_fetch[3])  # We get immediate
            return InstructionI(operation_code, Register(rt_name_register, 0), offset,
                                Register(rs_name_register, 0))  # Instance of I instruction
            # add $t2, $t2, $t1 => ['add', '$t2,', '$t2,', '$t1']
        elif operation_code in ["add", "sub", "rem", "mul"]:  # Type R
            rd_name_register = re.sub(",", "", instruction_array_fetch[1])  # We remove extra commas in rd
            rs_name_register = re.sub(",", "", instruction_array_fetch[2])  # We remove extra commas in rs
            rt_name_register = instruction_array_fetch[3]  # We remove extra commas in rt
            return InstructionR(operation_code, Register(rd_name_register, 0), Register(rs_name_register, 0),
                                Register(rt_name_register, 0))  # Instance of R instruction
        # j Potencia => ['j', 'Potencia']
        elif operation_code == "j":  # Type J
            target = self.labels[instruction_array_fetch[1]]  # We get memory address
            return InstructionJ(operation_code, target)  # Instance of J instruction
        # Potencia: beq $t6, $zero, FinBucle
        elif type(operation_code) == str:  # It's an instruction started by a label
            return self.create_instruction_for_if_id_register(instruction_array_fetch[1:], pc_address)
        else:
            raise ValueError

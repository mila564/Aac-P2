import os
import re

from Register import Register

from instructions.InstructionI import InstructionI
from instructions.InstructionJ import InstructionJ
from instructions.InstructionR import InstructionR

from pipeline_registers.IfIdPipelineRegister import IfIdPipelineRegister


class InstructionMemory:
    def __init__(self):
        self.__instructions = []
        self.__labels = {}
        with open(os.getcwd() + "/instructions.txt") as f:
            for linea in f:
                linea = linea.replace("\n", "")
                self.__instructions.append(linea)
        self.place_labels()

    @property
    def labels(self):
        s = "Labels: "
        for k, v in self.__labels.items():
            s += "{" + str(k) + ": " + str(v) + "} "
        return s

    def get_last_instruction_address(self):
        return len(self.__instructions) - 1

    def place_labels(self):
        for i in range(len(self.__instructions)):
            instruction_string = self.__instructions[i]
            instruction_array_string = instruction_string.split(" ")
            if not (instruction_array_string[0] in ["lw", "sw", "addi", "subi",
                                                    "beq", "add", "sub", "rem", "mul", "j"]):
                label = instruction_array_string[0]
                label = re.sub(":", "", label)
                self.__labels[label] = i

    def instruction_fetch(self, pc):
        if pc.address > self.get_last_instruction_address():
            return None
        instruction_array_fetch = str(self.__instructions[pc.address]).split()
        instruction_fetch = self.create_instruction_for_if_id_register(instruction_array_fetch, pc.address)
        return IfIdPipelineRegister(instruction_fetch)

    def create_instruction_for_if_id_register(self, instruction_array_fetch, pc_address):
        operation_code = instruction_array_fetch[0]
        if operation_code in ["lw", "sw", "beq", "addi", "subi"]:
            rt_name_register = re.sub(",", "", instruction_array_fetch[1])
            if operation_code in ["lw", "sw"]:
                offset_register = instruction_array_fetch[2]
                offset_register = offset_register.split("(")
                offset = int(offset_register[0])
                rs_name_register = offset_register[1]
                rs_name_register = re.sub("\\)", "", rs_name_register)
            elif operation_code == "beq":
                rs_name_register = re.sub(",", "", instruction_array_fetch[2])
                offset = self.__labels[instruction_array_fetch[3]]
            else:
                rs_name_register = re.sub(",", "", instruction_array_fetch[2])
                offset = int(instruction_array_fetch[3])
            return InstructionI(operation_code, Register(rt_name_register, 0), offset,
                                Register(rs_name_register, 0))
        elif operation_code in ["add", "sub", "rem", "mul"]:  # Type R
            rd_name_register = re.sub(",", "", instruction_array_fetch[1])
            rs_name_register = re.sub(",", "", instruction_array_fetch[2])
            rt_name_register = instruction_array_fetch[3]
            return InstructionR(operation_code, Register(rd_name_register, 0), Register(rs_name_register, 0),
                                Register(rt_name_register, 0))
        elif operation_code == "j":
            target = self.__labels[instruction_array_fetch[1]]
            return InstructionJ(operation_code, target)
        else:
            return self.create_instruction_for_if_id_register(instruction_array_fetch[1:], pc_address)

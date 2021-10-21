from ArithmeticLogicUnit import ArithmeticLogicUnit
from ProgramCounter import ProgramCounter
from InstructionMemory import InstructionMemory
from DataMemory import DataMemory
from RegisterFile import RegisterFile


def main():
    # datapath initialization
    pc = ProgramCounter()
    print(pc)
    im = InstructionMemory()
    im.print_instruction_memory_state()
    rf = RegisterFile()
    rf.print_register_file_state()
    alu = ArithmeticLogicUnit()
    dm = DataMemory()
    dm.print_data_memory_state()
    mem_wb = ex_mem = id_ex = if_id = None
    # loop
    while pc.address < im.get_last_instruction_address():
        rf.write_back(mem_wb)
        aux = alu.execution(id_ex, pc)
        mem_wb = dm.memory(ex_mem)
        ex_mem = aux
        id_ex = rf.instruction_decode(if_id)
        if_id = im.instruction_fetch(pc)
        pc.increment_pc()


if __name__ == '__main__':
    main()

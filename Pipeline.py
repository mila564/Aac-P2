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
    effective_jump, insert_bubble = False
    # loop
    while pc.address < im.get_last_instruction_address():
        rf.write_back(mem_wb)
        aux = alu.execution(id_ex, pc, effective_jump)
        mem_wb = dm.memory(ex_mem)
        ex_mem = aux
        id_ex = rf.instruction_decode(if_id, ex_mem.instruction, mem_wb, effective_jump, insert_bubble)
        # ex_mem and mem_wb parameter to check forwarding
        if_id = im.instruction_fetch(pc)  # Revise bubble thing in jumps and lw instruction in ex
        pc.increment_pc()
        effective_jump = False


if __name__ == '__main__':
    main()

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
    effective_jump = insert_bubble = False
    # loop
    while pc.address < im.get_last_instruction_address():
        rf.write_back(mem_wb)
        tuple_aux = alu.execution(id_ex, pc)  # tuple_aux = aux, effective_jump
        mem_wb = dm.memory(ex_mem)
        if tuple_aux is not None:
            aux = tuple_aux[0]
            effective_jump = tuple_aux[1]
            ex_mem = aux
        else:
            ex_mem = None
        tuple_id_ex = rf.instruction_decode(if_id, ex_mem, mem_wb, effective_jump)
        # tuple_id_ex = id_ex, insert_bubble
        if tuple_id_ex is not None:
            id_ex = tuple_id_ex[0]
            insert_bubble = tuple_id_ex[1]
        if_id = im.instruction_fetch(pc, insert_bubble, if_id)
        if not insert_bubble:
            pc.increment_pc()
        effective_jump = insert_bubble = False


if __name__ == '__main__':
    main()

from ArithmeticLogicUnit import ArithmeticLogicUnit
from ProgramCounter import ProgramCounter
from InstructionMemory import InstructionMemory
from DataMemory import DataMemory
from RegisterFile import RegisterFile


def print_state_components(pc, rf, dm):
    print(pc)
    rf.print_register_file_state()
    dm.print_data_memory_state()


def main():
    # datapath initialization
    pc = ProgramCounter()
    im = InstructionMemory()
    rf = RegisterFile()
    alu = ArithmeticLogicUnit()
    dm = DataMemory()
    mem_wb = ex_mem = id_ex = if_id = None
    effective_jump = insert_bubble = finished_pipeline = False
    # loop
    while not finished_pipeline:
        rf.write_back(mem_wb)
        tuple_aux = alu.execution(id_ex, pc)  # tuple_aux = ex_mem, effective_jump
        mem_wb = dm.memory(ex_mem)
        if tuple_aux is not None:
            ex_mem = tuple_aux[0]
            effective_jump = tuple_aux[1]
        else:
            ex_mem = None
        tuple_id_ex = rf.instruction_decode(if_id, ex_mem, mem_wb, effective_jump)
        # tuple_id_ex = id_ex, insert_bubble
        if tuple_id_ex is not None:
            id_ex = tuple_id_ex[0]
            insert_bubble = tuple_id_ex[1]
        else:
            id_ex = None
        if_id = im.instruction_fetch(pc, insert_bubble, if_id)
        if not insert_bubble and pc.address <= im.get_last_instruction_address():
            pc.increment_pc()
        print_state_components(pc, rf, dm)
        finished_pipeline = if_id == id_ex == ex_mem == mem_wb is None
        effective_jump = insert_bubble = False


if __name__ == '__main__':
    main()

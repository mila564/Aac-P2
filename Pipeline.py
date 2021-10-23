from ArithmeticLogicUnit import ArithmeticLogicUnit
from ProgramCounter import ProgramCounter
from InstructionMemory import InstructionMemory
from DataMemory import DataMemory
from RegisterFile import RegisterFile


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
        if mem_wb is not None:
            instruction_mem = mem_wb.instruction
        else:
            instruction_mem = None
        if tuple_aux is not None:
            ex_mem = tuple_aux[0]
            instruction_execution = ex_mem.instruction
            effective_jump = tuple_aux[1]
        else:
            ex_mem = instruction_execution = None
        tuple_id_ex = rf.instruction_decode(if_id, instruction_execution, instruction_mem, effective_jump)
        # tuple_id_ex = id_ex, insert_bubble
        if tuple_id_ex is not None:
            id_ex = tuple_id_ex[0]
            insert_bubble = tuple_id_ex[1]
        else:
            id_ex = None
        if_id = im.instruction_fetch(pc, insert_bubble, if_id)
        print_state(dm, ex_mem, id_ex, if_id, im, mem_wb, pc, rf)
        if not insert_bubble and pc.address <= im.get_last_instruction_address():
            pc.increment_pc()
        finished_pipeline = if_id == id_ex == ex_mem == mem_wb is None
        effective_jump = insert_bubble = False


def print_state(dm, ex_mem, id_ex, if_id, im, mem_wb, pc, rf):
    print("----------------")
    print(pc)
    print("----Pipeline----")
    print(mem_wb)
    print(ex_mem)
    print(id_ex)
    print(if_id)
    print("----------------")
    print(dm)
    print(rf)
    print(im.labels)
    print("----------------")


if __name__ == '__main__':
    main()

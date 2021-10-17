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
    dm = DataMemory()
    dm.print_data_memory_state()
    mem_wb = ex_mem = id_ex = if_id = None
    # loop
    '''
    while (pc.getAddress() < im.getLastInstructionAddress()):
        writeBack(mem_wb)
        ex_mem = execution(id_ex) # aux = execution(id_ex, pc)
        mem_wb = memory(ex_mem)
        # ex_mem = aux
        id_ex = instructionDecode(if_id)
        if_id = im.instructionFetch(pc)
        pc.incrementPc()
    '''


if __name__ == '__main__':
    main()

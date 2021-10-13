class InstructionMemory:
    def __init__(self):
        self.instructions = []
        with open('/instrucciones.txt') as f:
            for linea in f:
                self.instructions.append(f.read())
    def printInstructionMemoryState(self):
        print("Instruction Memory: ")
        for i in self.instructions:
            print(i)

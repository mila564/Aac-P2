class DataMemory:
    def __init__(self):
        self.data = []
        for i in range(32):
            self.data.append(0)
    def printDataMemoryState(self):
        print("Data Memory: ")
        for i in range(32):
            print("Posición " + str(i) + ": " + str(self.data[i]))
'''
dataMem = DataMemory()
dataMem.printDataMemoryState()
'''
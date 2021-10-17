class DataMemory:
    def __init__(self):
        self.data = []
        for i in range(58):
            self.data.append(0)

    def print_data_memory_state(self):
        print("Data Memory: ")
        for i in range(58):
            print("Index " + str(i) + ": " + str(self.data[i]))


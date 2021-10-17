class ProgramCounter:
    def __init__(self):
        self.address = 0

    def get_address(self):
        return self.address

    def set_address(self, address):
        try:
            self.address = int(address)
        except TypeError:
            print("Invalid type")

    def increment_pc(self):
        self.address += 1

    def __str__(self):
        return "PC = " + str(self.address)

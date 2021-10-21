class ProgramCounter:
    def __init__(self):
        self.__address = 0

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, a):
        self.__address = a

    def increment_pc(self):
        self.__address += 1

    def __str__(self):
        return "PC = " + str(self.__address)

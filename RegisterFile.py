class Register:
    def __init__(self, name, number, value):
        self.name = name
        self.number = number
        self.value = value
    def getName(self):
        return self.name
    def getNumber(self):
        return self.number
    def getValue(self):
        return self.value

class RegisterFile:
    def __init__(self):
        registerNames = ["$zero", "$at", "$v0", "$v1", "$a0", "$a1",
                         "$a2", "$a3", "$t0", "$t1", "$t2", "$t3",
                         "$t4", "$t5", "$t6", "$t7", "$s0", "$s1",
                         "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
                         "$t8", "$t9", "$k0", "$k1", "$gp", "$sp",
                         "$fp", "$ra"]
        self.registerFile = []
        for i in range(32):
            self.registerFile.append(Register(registerNames[i], i, 0))

    def printRegisterFileState(self):
        print("Register File: ")
        for i in range(32):
            print(self.registerFile[i].getName() + "|" + str(self.registerFile[i].getNumber()) + "|" + str(self.registerFile[i].getValue()))
'''
rf = RegisterFile()
rf.printRegisterFileState()
test = Register(("$zero"), 0, 0)
print(type(test))
'''
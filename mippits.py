#!/usr/bin/env python3

code = "00001020afc2fffcafc5fff8afdffff4000028140000000c03c5f02200001814ffffffff104300260000a014000000300282a0200000a814ffff000caeb400000042102000421020002220208c8200040000a014000000410282a0200000a814ffff000caeb400000000f8140000000403e00009006028208c8200080000a014000000410282a0200000a814ffff000caeb400000000f8140000000403e000090060202000a018200064102a1040000100801820000010140000000100621820000028140000000c03c5f0208fdffff48fc5fff88fc2fffc03e000080000a014000000410000a814ffff000caeb40000"

PC = 0
HI, LO = 0, 0
registers = [0] * 32

from collections import defaultdict
MEM = defaultdict(int)

def normalize(value):
    return value & 0xFFFFFFFF
def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value

# loader
assert len(code) % 8 == 0
for i in range(0, len(code) // 8):
    MEM[i] = int(code[i * 8:i * 8 + 8], 16)
registers[30] = 0xFFFFFFFC
registers[31] = 0xFFFFFFFC

def decode_execute(instruction):
    global PC
    registers[0] = 0
    d, s, t = (instruction >> 11) & 0b11111, (instruction >> 21) & 0b11111, (instruction >> 16) & 0b11111
    i = instruction & 0b1111111111111111
    if i & 0x8000: i -= 0x10000
    if instruction >> 26 == 0b000000 and instruction & 0b11111111111 == 0b00000100000: # add (add)
        registers[d] = normalize(registers[s] + registers[t])
    elif instruction >> 26 == 0b000000 and instruction & 0b11111111111 == 0b00000100010: # subtract (sub)
        registers[d] = normalize(registers[s] - registers[t])
    elif instruction >> 26 == 0b000000 and instruction & 0b1111111111111111 == 0b0000000000011000: # multiply (mult)
        result = signed(registers[s]) * signed(registers[t])
        HI, LO = result >> 32, result & 0xFFFFFFFF
    elif instruction >> 26 == 0b000000 and instruction & 0b1111111111111111 == 0b0000000000011001: # multiply unsigned (multu)
        result = registers[s] * registers[t]
        HI, LO = result >> 32, result & 0xFFFFFFFF
    elif instruction >> 26 == 0b000000 and instruction & 0b1111111111111111 == 0b0000000000011010: # divide (div)
        HI, LO = signed(registers[s]) % signed(registers[t]), signed(registers[s]) / signed(registers[t])
    elif instruction >> 26 == 0b000000 and instruction & 0b1111111111111111 == 0b0000000000011011: # divide unsigned (divu)
        HI, LO = registers[s] / registers[t], registers[s] / registers[t]
    elif instruction >> 16 == 0b0000000000000000 and instruction & 0b11111111111 == 0b00000010000: # move from high/remainder (mfhi)
        registers[d] = HI
    elif instruction >> 16 == 0b0000000000000000 and instruction & 0b11111111111 == 0b00000010010: # move from low/quotient (mflo)
        registers[d] = LO
    elif instruction >> 16 == 0b0000000000000000 and instruction & 0b11111111111 == 0b00000010100: # load immediate and skip (lis)
        assert PC % 4 == 0
        registers[d] = MEM[PC // 4]
        PC += 4
    elif instruction >> 26 == 0b100011: # load word (lw)
        address = registers[s] + i
        assert address % 4 == 0
        #wip: read from stdin when loading from 0xFFFF0004
        print("a", address // 4, "a")
        registers[t] = MEM[address // 4]
    elif instruction >> 26 == 0b101011: # store word (sw)
        address = registers[s] + i
        assert address % 4 == 0
        if address == 0xFFFF000C: print(chr(registers[t] & 0xFF), end="")
        MEM[address // 4] = registers[t]
    elif instruction >> 26 == 0b000000 and instruction & 0b11111111111 == 0b00000101010: # set less than (slt)
        registers[d] = 1 if signed(registers[s]) < signed(registers[t]) else 0
    elif instruction >> 26 == 0b000000 and instruction & 0b11111111111 == 0b00000101011: # set less than unsigned (sltu)
        registers[d] = 1 if registers[s] < registers[t] else 0
    elif instruction >> 26 == 0b000100: # branch on equal (beq)
        if registers[s] == registers[t]: PC += i * 4
    elif instruction >> 26 == 0b000101: # branch on not equal (bne)
        if registers[s] != registers[t]: PC += i * 4
    elif instruction >> 26 == 0b000000 and instruction & 0b111111111111111111111 == 0b000000000000000001000: # jump register (jr)
        PC = registers[s]
    elif instruction >> 26 == 0b000000 and instruction & 0b111111111111111111111 == 0b000000000000000001001: # jump and link register (jalr)
        temp = registers[s]
        registers[31] = PC
        PC = temp
    else: raise Exception("Unknown instruction: " + instruction)

while True:
    assert PC % 4 == 0
    if PC == 0xFFFFFFFC: break # jumped to the end location, terminate program
    instruction = MEM[PC // 4]
    PC += 4
    
    try:
        decode_execute(instruction)
    except: break

print(registers)

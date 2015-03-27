#!/usr/bin/env python3

def normalize(value):
    return value & 0xFFFFFFFF
def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value

# from http://code.activestate.com/recipes/577977-get-single-keypress/, MIT licensed
try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try: import msvcrt
    except ImportError: raise ImportError("getch not available")
    else: getch = msvcrt.getch
else:
    import sys
    def getch():
        """
        getch() -> key character

        Read a single keypress from stdin and return the resulting character. Nothing is echoed to the console. This call will block if a keypress is not already available, but will not wait for Enter to be pressed. 

        If the pressed key was a modifier key, nothing will be detected; if it were a special function key, it may return the first character of of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally: termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class Mippit:
    def __init__(self):
        self.registers = [0] * 32
        self.PC = 0
        self.HI, self.LO = 0, 0
        self.MEM = {}
        
        self.offset = self.PC
        self.tracing = False
    
    def trace(self, instruction, comment = None):
        if not self.tracing: return # tracing disabled
        if comment is None:
            print(instruction)
        else:
            print("[DEBUGGER] {:=#010x}    {:<20}; {}".format(self.offset, instruction, comment))
    
    def decode_execute(self, instruction):
        r = self.registers
        r[0] = 0 # reset the 0 register
        d, s, t = (instruction >> 11) & 0b11111, (instruction >> 21) & 0b11111, (instruction >> 16) & 0b11111
        i = instruction & 0b1111111111111111
        if i & 0x8000: i -= 0x10000 # make sure we interpret the value as a signed 16 bit integer
        
        if instruction & 0b11111100000000000000011111111111 == 0b00000000000000000000000000100000: # add (add)
            r[d] = normalize(r[s] + r[t])
            self.trace("add ${}, ${}, ${}".format(d, s, t), "${}={}, ${}={}, ${}={}".format(d, r[d], s, r[s], t, r[t]))
        elif instruction & 0b11111100000000000000011111111111 == 0b00000000000000000000000000100010: # subtract (sub)
            r[d] = normalize(r[s] - r[t])
            self.trace("sub ${}, ${}, ${}".format(d, s, t), "${}={}, ${}={}, ${}={}".format(d, r[d], s, r[s], t, r[t]))
        elif instruction & 0b11111100000000001111111111111111 == 0b00000000000000000000000000011000: # multiply (mult)
            result = signed(r[s]) * signed(r[t])
            self.HI, self.LO = normalize(result >> 32), normalize(result)
            self.trace("mult ${}, ${}".format(s, t), "${}={}, ${}={}".format(s, r[s], t, r[t]))
        elif instruction & 0b11111100000000001111111111111111 == 0b00000000000000000000000000011001: # multiply unsigned (multu)
            result = r[s] * r[t]
            self.HI, self.LO = normalize(result >> 32), normalize(result)
            self.trace("multu ${}, ${}".format(s, t), "${}={}, ${}={}".format(s, r[s], t, r[t]))
        elif instruction & 0b11111100000000001111111111111111 == 0b00000000000000000000000000011010: # divide (div)
            self.HI, self.LO = normalize(signed(r[s]) % signed(r[t])), normalize(signed(r[s]) // signed(r[t]))
            self.trace("div ${}, ${}".format(s, t), "${}={}, ${}={}".format(s, r[s], t, r[t]))
        elif instruction & 0b11111100000000001111111111111111 == 0b00000000000000000000000000011011: # divide unsigned (divu)
            self.HI, self.LO = r[s] % r[t], r[s] // r[t]
            self.trace("divu ${}, ${}".format(s, t), "${}={}, ${}={}".format(s, r[s], t, r[t]))
        elif instruction & 0b11111111111111110000011111111111 == 0b00000000000000000000000000010000: # move from high/remainder (mfhi)
            r[d] = self.HI
            self.trace("mfhi ${}".format(d), "${}={}".format(d, r[d]))
        elif instruction & 0b11111111111111110000011111111111 == 0b00000000000000000000000000010010: # move from low/quotient (mflo)
            r[d] = self.LO
            self.trace("mflo ${}".format(d), "${}={}".format(d, r[d]))
        elif instruction & 0b11111111111111110000011111111111 == 0b00000000000000000000000000010100: # load immediate and skip (lis)
            assert self.PC % 4 == 0
            r[d] = self.MEM[self.PC // 4] if self.PC // 4 in self.MEM else 0
            self.PC = normalize(self.PC + 4)
            self.trace("lis ${}".format(d), "${}={}".format(d, r[d]))
            self.trace(".word {}".format(r[d]))
        elif instruction & 0b11111100000000000000000000000000 == 0b10001100000000000000000000000000: # load word (lw)
            address = normalize(r[s] + i)
            assert address % 4 == 0
            if address == 0xFFFF0004: # read from stdin
                value = ord(getch())
                assert 0 <= value <= 255, "Invalid character entered - character must be ASCII"
                r[t] = value
            else: r[t] = self.MEM[address // 4] if address // 4 in self.MEM else 0
            self.trace("lw ${}, {}(${})".format(t, i, s), "${}={}, ${}={}".format(t, r[t], s, r[s]))
        elif instruction & 0b11111100000000000000000000000000 == 0b10101100000000000000000000000000: # store word (sw)
            address = normalize(r[s] + i)
            assert address % 4 == 0, "Invalid address - not aligned to word boundary."
            if address == 0xFFFF000C: # write to stdout
                print(chr(r[t] & 0xFF), end="")
            else: self.MEM[address // 4] = r[t]
            self.trace("sw ${}, {}(${})".format(t, i, s), "${}={}, ${}={}".format(t, r[t], s, r[s]))
        elif instruction & 0b11111100000000000000011111111111 == 0b00000000000000000000000000101010: # set less than (slt)
            r[d] = 1 if signed(r[s]) < signed(r[t]) else 0
            self.trace("slt ${}, ${}, ${}".format(d, s, t), "${}={}, ${}={}, ${}={}".format(d, r[d], s, r[s], t, r[t]))
        elif instruction & 0b11111100000000000000011111111111 == 0b00000000000000000000000000101011: # set less than unsigned (sltu)
            r[d] = 1 if r[s] < r[t] else 0
            self.trace("sltu ${}, ${}, ${}".format(d, s, t), "${}={}, ${}={}, ${}={}".format(d, r[d], s, r[s], t, r[t]))
        elif instruction & 0b11111100000000000000000000000000 == 0b00010000000000000000000000000000: # branch on equal (beq)
            if r[s] == r[t]: self.PC = normalize(self.PC + i * 4)
            self.trace("beq ${}, ${}, {}".format(s, t, i), "${}={}, ${}={}".format(s, r[s], t, r[t]))
        elif instruction & 0b11111100000000000000000000000000 == 0b00010100000000000000000000000000: # branch on not equal (bne)
            if r[s] != r[t]: self.PC = normalize(self.PC + i * 4)
            self.trace("bne ${}, ${}, {}".format(s, t, i), "${}={}, ${}={}".format(s, r[s], t, r[t]))
        elif instruction & 0b11111100000111111111111111111111 == 0b00000000000000000000000000001000: # jump register (jr)
            self.PC = r[s]
            self.trace("jr ${}".format(s), "${}={}".format(s, r[s]))
        elif instruction & 0b11111100000111111111111111111111 == 0b00000000000000000000000000001001: # jump and link register (jalr)
            temp = r[s]
            r[31] = self.PC
            self.PC = temp
            self.trace("jalr ${}".format(s), "${}={}".format(s, r[s]))
        else: raise Exception("Unknown instruction: {:=#010x}".format(instruction))
    
    def load(self, code, offset = 0): # load binary code into memory
        import struct
        assert len(code) % 4 == 0, "Invalid code length - machine code must be collection of 32-bit words"
        assert offset % 4 == 0, "Invalid offset - offset must be aligned to 32-bit word boundary"
        offset //= 4 # get the offset in words
        for i in range(0, len(code) // 4): # copy the code into memory
            self.MEM[i + offset] = struct.unpack(">i", code[i * 4:i * 4 + 4])[0] # load as big endian 32-bit integer
        self.registers[30] = 0x00000000
        self.registers[31] = 0xFFFFFFFF
    
    def load_hex(self, hex_code, offset = 0): # load hex code into memory
        assert len(hex_code) % 8 == 0, "Invalid code length - machine code must be collection of 32-bit words"
        assert offset % 4 == 0, "Invalid offset - offset must be aligned to 32-bit word boundary"
        offset //= 4
        for i in range(0, len(hex_code) // 8): # copy the code into memory
            self.MEM[i + offset] = int(hex_code[i * 8:i * 8 + 8], 16)
        self.registers[30] = 0x00000000
        self.registers[31] = 0xFFFFFFFF
    
    def step(self):
        if self.PC == 0xFFFFFFFF: return False # jumped past end of memory, program ended
        assert self.PC % 4 == 0, "Program counter must be aligned to word boundaries"
        instruction = self.MEM[self.PC // 4] if self.PC // 4 in self.MEM else 0
        self.offset = self.PC
        self.PC = normalize(self.PC + 4)
        self.decode_execute(instruction)
        return True
    
    def run(self, offset = 0):
        self.PC = offset
        while self.step(): pass

if __name__ == "__main__":
    mips = Mippit()
    mips.load_hex("00201820004008200060102003e00008")
    mips.registers[1], mips.registers[2] = 3, 4
    mips.run()
    print(mips.registers)

#!/usr/bin/env python3

import sys, getopt

import mippits

def breakpoint_prompt():
    print("[DEBUGGER] Program hit breakpoint at {:=#010x}".format(mips.PC))
    while True:
        try: values = input("[DEBUGGER] Enter a debugger command (or \"help\" for options): ").strip().split(maxsplit=1)
        except EOFError: sys.exit()
        command, param = values[0], values[1] if len(values) > 1 else None
        if command == "q" or command == "quit": # stop executing program
            sys.exit()
        elif command == "h" or command == "help": # show commands help
            print("q/quit          - stop debugging and exit")
            print("h/help          - show this help text")
            print("b [address]     - toggle breakpoint at current location, or optionally, at a specified address")
            print("c               - continue executing program")
            print("n               - run until just before the next physical instruction, then break")
            print("s               - run until just before the next instruction, then break")
            print("p [start[ end]] - print out register values and optionally, memory values between the specified address or addresses")
            print("w start         - set memory to values prompted from user starting from `start`")
            print("r reg value     - set register $`reg` to `value`")
            print("t               - toggle instruction tracing")
        elif command == "b":
            if not param: param = mips.PC
            try:
                location = int(param, 0) // 4
                if location in breakpoints:
                    breakpoints.remove(location)
                    print("[DEBUGGER] Breakpoint removed from {:=#010x}".format(location))
                else:
                    breakpoints.add(location)
                    print("[DEBUGGER] Breakpoint added at {:=#010x}".format(location))
            except ValueError: print("Invalid address: {}".format(param))
        elif command == "c": # continue executing program
            print("[DEBUGGER] Execution continuing from {:=#010x}".format(mips.PC))
            break
        elif command == "n": # step over (execute until the next instruction in memory)
            instruction = self.MEM[self.PC // 4] if self.PC // 4 in self.MEM else 0
            if instruction & 0b11111111111111110000011111111111 == 0b00000000000000000000000000010100: # load immediate and skip instruction, make sure to jump over the word
                location = mips.PC + 8
            else:
                location = mips.PC + 4
            breakpoints.add(location) # add a breakpoint at the next instruction in memory
            print("[DEBUGGER] Stepping over, breaking again at {:=#010x}".format(location))
            break
        elif command == "s": # step into (execute one instruction)
            if not mips.step(): break
        elif command == "p": # print
            print(" $1 = {:<25}  $2 = {:<25}  $3 = {:<25}  $4 = {:<20}".format(
                "{0:=#010x} ({0})".format(mips.registers[1]), "{0:=#010x} ({0})".format(mips.registers[2]),
                "{0:=#010x} ({0})".format(mips.registers[3]), "{0:=#010x} ({0})".format(mips.registers[4])
            ))
            print(" $5 = {:<25}  $6 = {:<25}  $7 = {:<25}  $8 = {:<20}".format(
                "{0:=#010x} ({0})".format(mips.registers[5]), "{0:=#010x} ({0})".format(mips.registers[6]),
                "{0:=#010x} ({0})".format(mips.registers[7]), "{0:=#010x} ({0})".format(mips.registers[8])
            ))
            print(" $9 = {:<25} $10 = {:<25} $11 = {:<25} $12 = {:<20}".format(
                "{0:=#010x} ({0})".format(mips.registers[9]), "{0:=#010x} ({0})".format(mips.registers[10]),
                "{0:=#010x} ({0})".format(mips.registers[11]), "{0:=#010x} ({0})".format(mips.registers[12])
            ))
            print("$13 = {:<25} $14 = {:<25} $15 = {:<25} $16 = {:<20}".format(
                "{0:=#010x} ({0})".format(mips.registers[13]), "{0:=#010x} ({0})".format(mips.registers[14]),
                "{0:=#010x} ({0})".format(mips.registers[15]), "{0:=#010x} ({0})".format(mips.registers[16])
            ))
            print("$17 = {:<25} $18 = {:<25} $19 = {:<25} $20 = {:<20}".format(
                "{0:=#010x} ({0})".format(mips.registers[17]), "{0:=#010x} ({0})".format(mips.registers[18]),
                "{0:=#010x} ({0})".format(mips.registers[19]), "{0:=#010x} ({0})".format(mips.registers[20])
            ))
            print("$21 = {:<25} $22 = {:<25} $23 = {:<25} $24 = {:<20}".format(
                "{0:=#010x} ({0})".format(mips.registers[21]), "{0:=#010x} ({0})".format(mips.registers[22]),
                "{0:=#010x} ({0})".format(mips.registers[23]), "{0:=#010x} ({0})".format(mips.registers[24])
            ))
            print("$25 = {:<25} $26 = {:<25} $27 = {:<25} $28 = {:<20}".format(
                "{0:=#010x} ({0})".format(mips.registers[25]), "{0:=#010x} ({0})".format(mips.registers[26]),
                "{0:=#010x} ({0})".format(mips.registers[27]), "{0:=#010x} ({0})".format(mips.registers[28])
            ))
            print("$29 = {:<25} $30 = {:<25} $31 = {:<25}".format(
                "{0:=#010x} ({0})".format(mips.registers[29]), "{0:=#010x} ({0})".format(mips.registers[30]),
                "{0:=#010x} ({0})".format(mips.registers[31])
            ))
            
            if param: # address value specified
                print()
                bounds = param.strip().split(maxsplit=1)
                try:
                    start, end = int(bounds[0], 0) // 4, int(int(bounds[1] if len(bounds) > 1 else bounds[0], 0) / 4 + 1) # lower and upper word boundaries
                except ValueError:
                    print("[DEBUGGER] Invalid address bounds: {}".format(param))
                else:
                    for location in range(start, end):
                        print("{0:=#010x} = {1:=#010x} ({1})".format(location * 4, mips.MEM[location] if location in mips.MEM else 0))
        elif command == "w":
            try:
                location = int(param, 0) // 4
            except ValueError:
                print("[DEBUGGER] Invalid start address: {}".format(param))
            else:
                while True:
                    entry = input("[DEBUGGER] Enter a value for memory at {:=#010x} (blank to end): ".format(location * 4))
                    try:
                        value = mippits.normalize(int(entry, 0))
                    except ValueError:
                        if entry.strip() == "": break
                        print("[DEBUGGER] Invalid value: '{}'".format(entry))
                    else:
                        print("[DEBUGGER] Memory at {0:=#010x} set to {1:=#010x} ({1})".format(location * 4, value))
                        mips.MEM[location] = value
                        location += 1
        elif command == "r":
            try:
                params = param.strip().split(maxsplit=1)
                register, value = int(params[0]), mippit.normalize(int(params[1], 0))
                assert 0 <= register <= 31, "Invalid register: {}".format(register)
                mips.registers[register] = value
                print("[DEBUGGER] Register ${0} set to {1:=#010x} ({1})".format(register, value))
            except:
                print("[DEBUGGER] Invalid register/value: {}".format(param))
        elif command == "t":
            if mips.tracing:
                mips.tracing = False
                print("[DEBUGGER] Instruction tracing disabled")
            else:
                mips.tracing = True
                print("[DEBUGGER] Instruction tracing enabled")
        else: print("[DEBUGGER] Unrecognized command: {}".format(command))

def print_help():
    print("{} --help".format(sys.argv[0]))
    print("    Shows this help message.")
    print()
    print("{} [--trace] [--breakpoints=b_1,...,b_n] file       ".format(sys.argv[0]))
    print("    Starts debugging `file`. If `--trace` is specified, instruction tracing is enabled.")
    print("    Breakpoints can be specified as `b_1,...,b_n` where each `b_1` to `b_n` is an address.")

# parse command line arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["help", "trace", "breakpoints="])
except getopt.GetoptError as err:
    print(err)
    print()
    print_help()
    sys.exit(2)
trace = False
breakpoints = set()
for opt, arg in opts:
    if opt == "--help":
        print_help()
        sys.exit()
    elif opt == "--trace":
        trace = True
    elif opt == "--breakpoints":
        breakpoints = set(int(x, 0) for x in arg.split(","))
if len(args) != 1:
    print_help()
    sys.exit(2)
file_path = args[0]
#wip: memory and register loading from options

mips = mippits.Mippit()
mips.tracing = trace # enable or disable tracing
try:
    with open(file_path, "rb") as f:
        code = f.read()
        mips.load(code)
except OSError:
    print("[DEBUGGER] Could not read file: {}".format(file_path))

# add breakpoints from the code
BREAKPOINT = 0x00000020 # this represents the instruction `add $0, $0, $0` and is interpreted as a breakpoint, since it is otherwise a no-op
for offset, instruction in mips.MEM.items():
    if instruction == BREAKPOINT:
        breakpoints.add(offset * 4)

while True:
    if mips.PC in breakpoints: breakpoint_prompt()
    if not mips.step(): break

breakpoint_prompt()

print("[DEBUGGER] Program exited normally.")

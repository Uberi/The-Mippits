#!/usr/bin/env python3

import sys, getopt

import mippits

# parse command line arguments
def print_help(): print("Usage: {} < MIPS_ASSEMBLED.mips > MIPS_DISASSEMBLED.asm".format(sys.argv[0]), file=sys.stderr)
try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["help"])
except getopt.GetoptError as err:
    print_help()
    sys.exit(2)
for opt, arg in opts:
    if opt == "--help":
        print_help()
        sys.exit()
if len(args) != 0:bash
    print_help()
    sys.exit(2)

code = sys.stdin.buffer.read()
words = mippits.code_to_words(code)
index = 0
while index < len(words):
    assembly_instruction = mippits.decode(words[index])
    print(assembly_instruction)
    if assembly_instruction.startswith("lis "): # load immediate and skip is always followed by a literal word
        if index < len(words) - 1: # there is a word after this one
            index += 1 # move to the literal word
            print(".word 0x{:X}".format(words[index])) # display the literal word
    index += 1 # move to the next word

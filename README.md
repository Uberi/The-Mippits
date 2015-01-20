The Mippits
===========

Flexible [MIPS](https://en.wikipedia.org/wiki/MIPS_instruction_set) **virtual machine** and **GDB-style debugger** with support for the [CS241](https://www.student.cs.uwaterloo.ca/~cs241/) MIPS instruction subset.

Rationale
---------

The CS241 course at the University of Waterloo, "Foundations of Sequential Programs", provides various tools for working with MIPS executables, which are a large part of assignments and coursework.

However, they are strongly coupled with the student Linux environment, which makes it very difficult to work offline. If something goes wrong, one has very few tools to figure out what the problem is.

MIPPET is a tiny, flexible, and extensible virtual machine to help alleviate these issues. The MIPPET debugger supports **breakpoints**, **stepping** (including stepping over calls), and **instruction/control flow tracing** with **inline value inspection**.

Setup
-----

First, make sure you have a recent version of [Python 3](https://www.python.org/downloads/).

Now, [download the software](https://github.com/Uberi/The-Mippits/archive/master.zip) and extract it.

Using the Debugger
------------------

If your assignment is due Wednesday and your code is both totally broken and entirely opaque, this is probably what you're looking for.

Help:

    $ ./debugger.py --help
    debugger.py --help
        Shows this help message.
    
    debugger.py [--trace] [--breakpoints=b_1,...,b_n] file
        Starts debugging `file`. If `--trace` is specified, instruction tracing is enabled.
        Breakpoints can be specified as `b_1,...,b_n` where each `b_1` to `b_n` is an address.

Standard debugging:

    $ ./debugger.py --breakpoints=0 swap_r1_and_r2.mips
    [DEBUGGER] Program hit breakpoint at 0x00000000
    Enter a debugger command (or "help" for options): help
    q/quit          - stop debugging and exit
    h/help          - show this help text
    b [address]     - toggle breakpoint at current location, or optionally, at a specified address
    c               - continue executing program
    n               - run until just before the next physical instruction, then break
    s               - run until just before the next instruction, then break
    p [start[ end]] - print out register values and optionally, memory values between the specified address or addresses
    t               - toggle instruction tracing
    r reg value     - set register $`reg` to `value`
    Enter a debugger command (or "help" for options): r 1 54364
    Register $1 set to 0x0000D45C (54364)
    Enter a debugger command (or "help" for options): r 2 0x8
    Register $1 set to 0x00000008 (8)
    Enter a debugger command (or "help" for options): p
     $1 = 0x0000d45c (54364)         $2 = 0x00000008 (8)             $3 = 0x00000000 (0)             $4 = 0x00000000 (0)
     $5 = 0x00000000 (0)             $6 = 0x00000000 (0)             $7 = 0x00000000 (0)             $8 = 0x00000000 (0)
     $9 = 0x00000000 (0)            $10 = 0x00000000 (0)            $11 = 0x00000000 (0)            $12 = 0x00000000 (0)
    $13 = 0x00000000 (0)            $14 = 0x00000000 (0)            $15 = 0x00000000 (0)            $16 = 0x00000000 (0)
    $17 = 0x00000000 (0)            $18 = 0x00000000 (0)            $19 = 0x00000000 (0)            $20 = 0x00000000 (0)
    $21 = 0x00000000 (0)            $22 = 0x00000000 (0)            $23 = 0x00000000 (0)            $24 = 0x00000000 (0)
    $25 = 0x00000000 (0)            $26 = 0x00000000 (0)            $27 = 0x00000000 (0)            $28 = 0x00000000 (0)
    $29 = 0x00000000 (0)            $30 = 0xffffffff (4294967295)   $31 = 0xffffffff (4294967295)
    Enter a debugger command (or "help" for options): c
    Execution continuing from 0x00000000
    [DEBUGGER] Program hit breakpoint at 0xffffffff
    Enter a debugger command (or "help" for options): p
     $1 = 0x00000008 (8)             $2 = 0x0000d45c (54364)         $3 = 0x0000d45c (54364)         $4 = 0x00000000 (0)
     $5 = 0x00000000 (0)             $6 = 0x00000000 (0)             $7 = 0x00000000 (0)             $8 = 0x00000000 (0)
     $9 = 0x00000000 (0)            $10 = 0x00000000 (0)            $11 = 0x00000000 (0)            $12 = 0x00000000 (0)
    $13 = 0x00000000 (0)            $14 = 0x00000000 (0)            $15 = 0x00000000 (0)            $16 = 0x00000000 (0)
    $17 = 0x00000000 (0)            $18 = 0x00000000 (0)            $19 = 0x00000000 (0)            $20 = 0x00000000 (0)
    $21 = 0x00000000 (0)            $22 = 0x00000000 (0)            $23 = 0x00000000 (0)            $24 = 0x00000000 (0)
    $25 = 0x00000000 (0)            $26 = 0x00000000 (0)            $27 = 0x00000000 (0)            $28 = 0x00000000 (0)
    $29 = 0x00000000 (0)            $30 = 0xffffffff (4294967295)   $31 = 0xffffffff (4294967295)
    Enter a debugger command (or "help" for options): c
    Execution continuing from 0xffffffff
    [DEBUGGER] Program exited normally. 

License
-------

MIPPIT is MIT licensed and lives at https://github.com/Uberi/The-Mippits/. See the `LICENSE` file in the program directory for more information.

Although MIPPITS tries to be faithful to the execution environment given in the course materials, it is possible that the simulation is not perfect and there may be subtle differences in functionality. Use this software at your own risk.

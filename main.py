from lib2to3.pgen2.token import OP
import sys
import re

from FileReadWriter import FileReadWriter
from OpcodeParser import OpcodeParser
from utils.HexString import hex_str_to_int
from utils.ObjString import get_end_string, get_header_string, get_modification_string, get_text_string
from utils.Constant import get_bytes_of_constant
from utils.Instruction import generate_instruction_, get_instruction_length

DEBUG = False

REGTAB = {
    'A': 0,
    'X': 1,
    'L': 2,
    'B': 3,
    'S': 4,
    'T': 5,
    'F': 6,
}
OPTAB = opcodeParser = OpcodeParser('./OPTAB').get_OPTAB()
BASE = 0
LOCCTR = None

fileReaderWriter = FileReadWriter(*sys.argv[1:])
fileLines = fileReaderWriter.get_lines()

programName = ""
programAddressBase = None
programSize = 0
relativeAddressing = False
relocateList = []
SYMTAB = {}

# pass 1
for line in fileLines:
    tokens = line.split(" ")
    symbol = tokens[0]
    opcode = tokens[1]

    operand = tokens[2] if len(tokens) > 2 else None

    if opcode == 'START':
        programName = tokens[0]
        programAddressBase = hex_str_to_int(tokens[2])
        LOCCTR = programAddressBase
        relativeAddressing = True if programAddressBase == 0 else False
    
    elif opcode == 'END':
        programSize = LOCCTR - programAddressBase

    else:
        # symbol part
        if len(symbol) > 0: # if symbol already exists
            if symbol in SYMTAB:
                raise Exception(f'Symbol {symbol} already exist.')
            else:
                SYMTAB[symbol] = LOCCTR

        # opcode part
        if opcode in OPTAB or (opcode[0] == '+' and opcode[1:] in OPTAB):
            LOCCTR += get_instruction_length(opcode, OPTAB)
        elif opcode == 'WORD':
            LOCCTR += 3
        elif opcode == 'RESW':
            LOCCTR += 3 * int(operand)
        elif opcode == 'RESB':
            LOCCTR += int(operand)
        elif opcode == 'BYTE':
            LOCCTR += get_bytes_of_constant(operand)
        elif opcode == 'BASE':
            continue
        else:
            raise Exception(f'{opcode} not in OPTAB.')

if DEBUG:
    print(SYMTAB)

# pass 2
for line in fileLines:
    tokens = line.split(" ")

    symbol = tokens[0]
    opcode = tokens[1]
    operand = tokens[2] if len(tokens) > 2 else None

    if opcode == 'START':
        fileReaderWriter.write_line(get_header_string(programName, programAddressBase, programSize), append=False)
        LOCCTR = programAddressBase
        textStart = LOCCTR
        textBuffer = ""
    
    elif opcode == 'END':
        # output the string remain in buffer
        textString = get_text_string(textStart, textBuffer)
        if len(textString) > 0:
            fileReaderWriter.write_line(textString)

        # Modification record
        for address, length in relocateList:
            fileReaderWriter.write_line(get_modification_string(address, length))

        # write end string
        fileReaderWriter.write_line(get_end_string(programAddressBase))

    elif opcode == 'BASE':
        # set BASE register
        BASE = SYMTAB[operand] if operand[0] != '#' else int(operand[1:])

    else:
        lineAddress = LOCCTR

        # Update LOCCTR
        if opcode in OPTAB or (opcode[0] == '+' and opcode[1:] in OPTAB):
            LOCCTR += get_instruction_length(opcode, OPTAB)
        elif opcode == 'WORD':
            LOCCTR += 3
        elif opcode == 'BYTE':
            LOCCTR += get_bytes_of_constant(operand)
        elif opcode == 'RESW':
            LOCCTR += 3 * int(operand)
        elif opcode == 'RESB':
            LOCCTR += int(operand)


        # text buffer overflow
        if LOCCTR - textStart > 30:
            textString = get_text_string(textStart, textBuffer)
            if len(textString) > 0:
                fileReaderWriter.write_line(textString)

            textStart = lineAddress
            if opcode in ['RESW', 'RESB']:
                textBuffer = ""
            else:
                textBuffer = generate_instruction_(opcode, operand, OPTAB, SYMTAB, relativeAddressing, relocateList, lineAddress, REGTAB, LOCCTR, BASE)
        else:
            textBuffer += generate_instruction_(opcode, operand, OPTAB, SYMTAB, relativeAddressing, relocateList, lineAddress, REGTAB, LOCCTR, BASE)

        if DEBUG:
            print(f'opcode: {opcode}\noperand: {operand}\ninstruction: {generate_instruction_(opcode, operand, OPTAB, SYMTAB, relativeAddressing, relocateList, lineAddress, REGTAB, LOCCTR, BASE, DEBUG)}')
            input()
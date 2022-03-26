from utils.HexString import int_to_string_as_hex, hex_str_to_int
from utils.Constant import get_constant_hex

def get_instruction_length(opcode, OPTAB):
    if opcode[0] == '+':                    # format 4
        return 4
    elif OPTAB[opcode]['format'] == '1':    # format 1
        return 1
    elif OPTAB[opcode]['format'] == '2':    # format 2
        return 2
    else:                                   # format 3
        return 3


'''
relocateList would be modified
'''
def generate_instruction_(opcode, operand, OPTAB, SYMTAB, relativeAddressing, relocateList, lineAddress, REGTAB, LOCCTR, BASE, DEBUG=False):
    if opcode in ['RESW', 'RESB']:
        return ""

    # output operand as a constant
    if opcode == 'WORD':
        return f'{int_to_string_as_hex(int(operand)).zfill(6)}'
    if opcode == 'BYTE':
        return f'{get_constant_hex(operand)}'

    if opcode[0] != '+':
        intOpcode =  hex_str_to_int(OPTAB[opcode]['opcode'])
    else:
        intOpcode =  hex_str_to_int(OPTAB[opcode[1:]]['opcode'])

    instruction = 0

    if DEBUG:
        print(f'intOpcode: {intOpcode}')

    format = 0
    formatInstructionLength = [2, 4, 6, 8]

    if opcode[0] == '+':                    # format 4
        format = 4
        instruction = intOpcode << 24

        instruction += (1 << 25) + (1 << 24)                                # n + i
        instruction -= (1 << 24) if operand[0] == '@' else 0                # n
        instruction -= (1 << 25) if operand[0] == '#' else 0                # i
        if len(operand.split(',')) > 1 and operand.split(',')[-1] == 'X':   # x
            instruction += 1 << 23             
        instruction += 1 << 20                                              # e
            
        if operand[0] == '@' or operand[0] == '#':
            operand = operand[1:]

        if operand in SYMTAB:                                               # address
            instruction += SYMTAB[operand]
            if relativeAddressing:
                relocateList.append((lineAddress + 1, 5))
        else:
            instruction += int(operand)
        
        
    elif OPTAB[opcode]['format'] == '1':      # format 1
        format = 1
        instruction = intOpcode

    elif OPTAB[opcode]['format'] == '2':    # format 2
        format = 2
        instruction = intOpcode << 8
        operand = operand.split(',')
        instruction += (REGTAB[operand[0]] << 4) + (REGTAB[operand[1]] if len(operand) > 1 else 0)

    else:                                   # format 3
        format = 3
        instruction = intOpcode << 16
        
        if OPTAB[opcode]['oprandCount'] == 0:
            instruction += (1 << 17) + (1 << 16)                            # n + i
            return f'{int_to_string_as_hex(instruction).zfill(formatInstructionLength[format - 1])}'

        instruction += (1 << 17) + (1 << 16)                                # n + i
        instruction -= (1 << 16) if operand[0] == '@' else 0                # n
        instruction -= (1 << 17) if operand[0] == '#' else 0                # i
        if len(operand.split(',')) > 1 and operand.split(',')[-1] == 'X':   # x
            instruction += 1 << 15                  
        operand = operand.split(',')[0]

        if operand[0] == '@' or operand[0] == '#':
            operand = operand[1:]

        if operand in SYMTAB:                                               # b, p, disp
            if DEBUG:
                print(f'SYMTAB[operand]: {SYMTAB[operand]}, LOCCTR: {LOCCTR}')
                
            if SYMTAB[operand] - LOCCTR >= -2048 and SYMTAB[operand] - LOCCTR <= 2047:              # p
                instruction += 1 << 13
                if SYMTAB[operand] - LOCCTR >= 0:
                    instruction += SYMTAB[operand] - LOCCTR
                else:  # disp part need to be carefully processed because of representation of complement of negative number
                    instruction += ((1 << 12) - 1) & (SYMTAB[operand] - LOCCTR)

            elif SYMTAB[operand] - BASE >= 0 and SYMTAB[operand] - BASE <= 4095:  # b
                instruction += 1 << 14
                instruction += SYMTAB[operand] - BASE
            else:
                raise Exception(f'Must use foramt 4.')
            
        else:
            instruction += int(operand)

    return f'{int_to_string_as_hex(instruction).zfill(formatInstructionLength[format - 1])}'
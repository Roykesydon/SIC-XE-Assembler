from utils.HexString import int_to_string_as_hex

'''
return length of bytes of constant
'''
def get_bytes_of_constant(constant):
    if constant[0] == 'C':
        return len(constant) - 3
    elif constant[0] == 'X':
        return int((len(constant) - 3) / 2) 

'''
return constant as hex string
'''
def get_constant_hex(constant):
    if constant[0] == 'C':
        return "".join([int_to_string_as_hex((ord(char))).zfill(2) for char in constant[2:-1]])
    elif constant[0] == 'X':
        return constant[2:-1]
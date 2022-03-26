from utils.HexString import int_to_string_as_hex

def get_header_string(programName, programAddressBase, programSize):
    return f'H{programName.ljust(6)}{int_to_string_as_hex(programAddressBase).zfill(6)}{int_to_string_as_hex(programSize).zfill(6)}'

def get_end_string(programAddressBase):
    return f'E{int_to_string_as_hex(programAddressBase).zfill(6)}'

def get_text_string(textStart, textBuffer):
    if len(textBuffer) == 0:
        return ""
    return  f'T{int_to_string_as_hex(textStart).zfill(6)}{int_to_string_as_hex(int(len(textBuffer) / 2)).zfill(2)}{textBuffer}'

def get_modification_string(address, length):
    return f'M{int_to_string_as_hex(address).zfill(6)}{int_to_string_as_hex(length).zfill(2)}'
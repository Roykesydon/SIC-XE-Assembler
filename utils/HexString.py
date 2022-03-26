def hex_str_to_int(target):
    return int(target, 16)

def int_to_string_as_hex(target):
    return str(hex(target))[2:].upper()

# def test():
    # print(0x16) # 22
    # print(0x1 + 0x20) # 33
    # print(int_to_string_as_hex(32)) # 20
    # raise Exception('symbol already exist.')
    # print('1'.upper()) # 1
    # print('1a'.upper()) # 1A
    # pass
#Could probably do something more here where we overload this to either return a checksum or verify an existing checksum. Possibly need 2 functions?
def calc_crc8(byte_array, initialization, polynomial):
    crc = initialization
    polynomial = polynomial
    for byte in byte_array:
        crc ^= byte
        for bit in range(8):
            if crc & 0x80 != 0:
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
    return crc

def validatecrc_andreturn(byte_array, crc, initialization, polynomial):
    checksum = calc_crc8(byte_array, initialization, polynomial)
    if checksum == crc:
        #checksum is valid return true
        return True
    else:
        return False

def parse_crc8(byte_array, initialization, polynomial):
    byte_counter = 0
    parsed_byte_array = bytearray()
    temp_byte_array = bytearray(2)

    for byte in byte_array:
        #Check to see if we're looking at the checksum bit
        if byte_counter % 3 != 2:
            temp_byte_array[byte_counter] = byte
            byte_counter += 1
        else:
            byte_counter += 1
            #We're at the checksum bit so let's calculate it and make sure it's right
            if validatecrc_andreturn(temp_byte_array, byte, initialization, polynomial):
                parsed_byte_array.extend(temp_byte_array)
                temp_byte_array = bytearray(2)
                byte_counter = 0
            else:
                print("checksum failed")
    return parsed_byte_array
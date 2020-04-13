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
    return hex(crc)
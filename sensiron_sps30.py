import board, busio, crc8
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = '0.0.1'

## Addresses for commands


class SPS30:

    def __init__(self, i2c_bus, address=0x69, crc_init=0xFF, crc_poly=0x131):
        self.i2c_device = I2CDevice(i2c_bus, address)
        self.crc_init = crc_init
        self.crc_poly = crc_poly
        #Try to grab the serial number to ensure that we've got a connection
        cmd = bytearray([0xD0, 0x33])
        self.buf = bytearray(47)
        with self.i2c_device as i2c:
            i2c.write_then_readinto(cmd, self.buf)
        

    def getSerialNumber(self):
        #Try to grab the serial number to ensure that we've got a connection
        cmd = bytearray([0xD0, 0x33])
        buf = bytearray(47)
        with self.i2c_device as i2c:
            i2c.write_then_readinto(cmd, buf)
        #Return the raw bytes. We can do cool stuff with this later. 
        return(crc8.parse_crc8(buf, self.crc_init, self.crc_poly))
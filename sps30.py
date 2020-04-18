from adafruit_bus_device.i2c_device import I2CDevice
import crc8

def __init__(self, i2c_bus, address=0x69):
    self.i2c_device = I2CDevice(i2c_bus, address)


import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice

DEVICE_ADDRESS = 0x69  # device address of DS3231 board
A_DEVICE_REGISTER = [0xD0, 0x33]  # device id register on the DS3231 board

# The follow is for I2C communications
comm_port = busio.I2C(board.SCL, board.SDA)
device = I2CDevice(comm_port, DEVICE_ADDRESS)

with device as bus_device:
 bus_device.write(bytes([A_DEVICE_REGISTER]))
 result = bytearray(47)
 bus_device.readinto(result)

print("".join("{:02x}".format(x) for x in result))

#Review the datasheet here: https://cdn.sparkfun.com/assets/learn_tutorials/1/4/3/CCS811_Datasheet-DS000459.pdf
#and the source code here:https://circuitpython.readthedocs.io/projects/ccs811/en/latest/_modules/adafruit_ccs811.html#CCS811
# to attempt to reverse engineer
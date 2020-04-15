import board, busio
import struct
from adafruit_bus_device.i2c_device import I2CDevice
import time

def calcFloat(sixBArray):
  struct_float = struct.pack('>BBBB', sixBArray[0], sixBArray[1], sixBArray[3], sixBArray[4])
  float_values = struct.unpack('>f', struct_float)
  first = float_values[0]
  return first


with busio.I2C(board.SCL, board.SDA) as i2c:
    device = I2CDevice(i2c, 0x69)
    seq = bytearray([0x00, 0x10, 0x03, 0x00, 0xAC])
    with device:
        device.write(seq)
    ready_check = bytearray([0x02, 0x02, 0x3A])
    ready_result = bytearray(3)
    with device:
        device.write_then_readinto(ready_check, ready_result)
        time.sleep(2)
        print(ready_result)

    read_values_cmd = bytearray([0x03, 0x00, 0xAC])
    values = bytearray(600)
    with device:
        device.write_then_readinto(read_values_cmd, values)
        print(values)
        time.sleep(2)

output_string = 'particulate_matter_ppcm3{{size="pm0.5",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[24:30]))
output_string += 'particulate_matter_ppcm3{{size="pm1",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[30:36]))
output_string += 'particulate_matter_ppcm3{{size="pm2.5",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[36:42]))
output_string += 'particulate_matter_ppcm3{{size="pm4",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[42:48]))
output_string += 'particulate_matter_ppcm3{{size="pm10",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[48:54]))
#output_string += 'particulate_matter_ugpm3{{size="pm1",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values))
output_string += 'particulate_matter_ugpm3{{size="pm2.5",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[6:12]))
output_string += 'particulate_matter_ugpm3{{size="pm4",sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[12:18]))
#output_string += 'particulate_matter_ugpm3{{size="pm10",sensor="SPS30"}} {0:.8f}\n'.format( pm10 )
output_string += 'particulate_matter_typpartsize_um{{sensor="SPS30"}} {0:.8f}\n'.format( calcFloat(values[54:60]))
print(output_string)

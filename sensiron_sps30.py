import board, busio, crc8, struct
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = '0.0.1'

## Addresses for commands


class SPS30:

    def __init__(self, i2c_bus, address=0x69, crc_init=0xFF, crc_poly=0x131):
        self.i2c_device = I2CDevice(i2c_bus, address)
        self.crc_init = crc_init
        self.crc_poly = crc_poly
        #Try to grab the serial number to ensure that we've got a connection

    def calcFloat(self, byte_array):
        #Shamelessly stolen from the UnravelTec driver
        #TODO: Investigate using the struct library for other byte-bashing
        struct_float = struct.pack('>BBBB', byte_array[0], byte_array[1], byte_array[2], byte_array[3])
        return struct.unpack('>f', struct_float)[0]

    def parseMeasurement(self, measurement):
        measurement_obj = {}

        measurement_obj["Mass Concentration PM 1.0 [ug/m3]"] = self.calcFloat(measurement[0:4])
        measurement_obj["Mass Concentration PM 2.5 [ug/m3]"] = self.calcFloat(measurement[4:8])
        measurement_obj["Mass Concentration PM 4.0 [ug/m3]"] = self.calcFloat(measurement[8:12])
        measurement_obj["Mass Concentration PM 10 [ug/m3]"] = self.calcFloat(measurement[12:16])

        measurement_obj["Number Concentration PM 0.5 [#/m3]"] = self.calcFloat(measurement[16:20])
        measurement_obj["Number Concentration PM 1.0 [#/m3]"] = self.calcFloat(measurement[20:24])
        measurement_obj["Number Concentration PM 2.5 [#/m3]"] = self.calcFloat(measurement[24:28])
        measurement_obj["Number Concentration PM 4.0 [#/m3]"] = self.calcFloat(measurement[28:32])
        measurement_obj["Number Concentration PM 10 [#/m3]"] = self.calcFloat(measurement[32:36])

        measurement_obj["Typical Particle Size [um]"] = self.calcFloat(measurement[36:40])


        return measurement_obj

    def getSerialNumber(self):
        #Try to grab the serial number to ensure that we've got a connection
        cmd = bytearray([0xD0, 0x33])
        buf = bytearray(47)
        with self.i2c_device as i2c:
            i2c.write_then_readinto(cmd, buf)
        #FIXME: Return the raw bytes. We should parse this into a string. 
        return(crc8.parse_crc8(buf, self.crc_init, self.crc_poly))

    def startMeasurement(self):
        cmd = bytearray([0x00, 0x10, 0x03, 0x00, crc8.calc_crc8([0x03, 0x00], self.crc_init, self.crc_poly)])
        
        with self.i2c_device as i2c:
            i2c.write(cmd)

        #FIXME: Right now we just YOLO and assume everything is OK. In the future we should read the device's status (Section 6.3.11)    
    
    def readMeasurement(self):
        #First check to see if there is data ready
        cmd = bytearray([0x02, 0x02])
        #Setup a buffer to read into
        buf = bytearray(3)

        with self.i2c_device as i2c:
            i2c.write_then_readinto(cmd, buf)
        #Check the CRC and parse the data out. The flag that we want is always in the second bit
        data_ready =  crc8.parse_crc8(buf, self.crc_init, self.crc_poly)[1]

        print(buf)
        print(data_ready)

        if data_ready == 1:
            cmd = bytearray([0x03, 0x00])
            buf = bytearray(60)

            with self.i2c_device as i2c:
                i2c.write_then_readinto(cmd, buf)
            
            measurement = crc8.parse_crc8(buf, self.crc_init, self.crc_poly)
            print(measurement)
            parsed_measurement = self.parseMeasurement(measurement)
            return parsed_measurement
        else:
            return "Data not available"

    def reset(self):
        #FIXME: Unable to reactivate after sending the reset sequence.
        cmd = bytearray([0xD3, 0x04])

        with self.i2c_device as i2c:
            i2c.write(cmd)
        
#import storage to reset filesystem if needed

import board
import neopixel
import time
import math
import digitalio
import busio
import adafruit_bme280
import adafruit_ccs811
import sensiron_sps30

#Turn off the very obnoxious NeoPixel on boot.
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixels[0] = (0, 0, 0)

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)

# Connect devices to the i2c bus
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

#Sparkfun sensor uses a different address for the CCS sensor
#ccs = adafruit_ccs811.CCS811(i2c, address=0x5b)

#SPS library!
sps30 = sensiron_sps30.SPS30(i2c)

while True:
    minutes_awake = math.floor(time.monotonic()/60)
    print(sps30.getSerialNumber())
    '''print("Temperature: {:.2f} C".format(bme280.temperature))
    print("Humidity: {:.1f}%".format(bme280.humidity))
    print("Pressure: {:.1f} hPa".format(bme280.pressure))
    print("Minutes awake = {:d}".format(minutes_awake))
    if minutes_awake > 19 and ccs.data_ready:
        ccs.set_environmental_data(bme280.humidity, bme280.temperature)
        print("CO2: {} ppm".format(ccs.eco2))
        print("VOCs: {} ppb".format(ccs.tvoc))
    '''
    time.sleep(2)
    print("\n" * 20)
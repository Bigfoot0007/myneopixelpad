from machine import Pin, I2C
import si7021

## this project neopixelpad

__i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
__temp_sensor = si7021.Si7021(__i2c)

def temperature():
    return __temp_sensor.temperature


def humidity():
    return __temp_sensor.relative_humidity


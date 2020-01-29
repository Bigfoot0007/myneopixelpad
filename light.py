from machine import ADC,Pin

light_sensor=ADC(Pin(34))

def readlight():
  return int(light_sensor.read()/17)+1

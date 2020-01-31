# -*- coding: UTF-8 -*-
import net
import _thread
import time
import os
from machine import Timer,Pin
from myneopixelpad import MyNeoPixelPad


try:
  _thread.start_new_thread(net.connectwifi, ("JJHOME","flzx3000c"))
  myneo=MyNeoPixelPad(13)
  
  p0 = Pin(15, Pin.IN)
  p0.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:myneo.onclick())
  
  #print(wifi_thread)
  tim_led = Timer(1)
  tim_led.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:myneo.showtimeandth())
  
  # tim.init(period=2000, mode=Timer.PERIODIC, callback=lambda t:print(2))
  #_thread.start_new_thread(neopixel832.showtime,())

except:
  pass
  
print("  ===================    Boot Done     ====================")

# time.sleep(30)







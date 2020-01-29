
import time
# from machine import Pin RTC
import machine
import network
import ntptime


def connectwifi(SSID, PASS):
  led=machine.Pin(2, machine.Pin.OUT) # 灏唋ed寮曡剼瀹氫箟涓鸿緭鍑猴紝鏉胯浇LED
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  while True:
    try:
      if not wlan.isconnected():
          led.value(0)  # Off the LED
          print('connecting to network...%s' %(SSID))
          wlan.connect(SSID, PASS)
          time.sleep(1)
      else:
        if time.localtime()[0] < 2020 :  # 大于2020年，保证只请求一次，默认为2000
          ntptime.settime()
          print(time.localtime(time.mktime(time.localtime()) + 8*3600))
        led.value(not led.value())
        time.sleep(1)
    except:
      pass
            
if __name__ == '__main__' :
  print(__name__)
  print("..............Enter the main loop ........")
  # connectwifi("JJHOME","flzx3000c")




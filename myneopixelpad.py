# -*- coding: UTF-8 -*-
import machine, neopixel
import urandom
import time
import os
from light import *

class MyNeoPixelPad:
    XY=[
      [0,15,16,31,32,47,48,63,64,79,80,95,96,111,112,127,128,143,144,159,160,175,176,191,192,207,208,223,224,239,240,255],
      [1,14,17,30,33,46,49,62,65,78,81,94,97,110,113,126,129,142,145,158,161,174,177,190,193,206,209,222,225,238,241,254],
      [2,13,18,29,34,45,50,61,66,77,82,93,98,109,114,125,130,141,146,157,162,173,178,189,194,205,210,221,226,237,242,253],
      [3,12,19,28,35,44,51,60,67,76,83,92,99,108,115,124,131,140,147,156,163,172,179,188,195,204,211,220,227,236,243,252],
      [4,11,20,27,36,43,52,59,68,75,84,91,100,107,116,123,132,139,148,155,164,171,180,187,196,203,212,219,228,235,244,251],
      [5,10,21,26,37,42,53,58,69,74,85,90,101,106,117,122,133,138,149,154,165,170,181,186,197,202,213,218,229,234,245,250],
      [6,9,22,25,38,41,54,57,70,73,86,89,102,105,118,121,134,137,150,153,166,169,182,185,198,201,214,217,230,233,246,249],
      [7,8,23,24,39,40,55,56,71,72,87,88,103,104,119,120,135,136,151,152,167,168,183,184,199,200,215,216,231,232,247,248]]
    offcolor=(0,0,0)   # 关闭的颜色，或者背景颜色
    pixnumber=8*32  # pad size
    colors=[(0,1,0),(0,1,0),(1,0,0),(0,1,0),(0,1,0),(1,0,1),(1,0,1)]  # 一共7个字符，每个字符显示的颜色。
    def __init__(self,PIN=13,backgroundcolor=(0,0,0)):
        print(" The Neopixel using %s"%PIN)
        self.PIN=PIN  # 对应的PIN，GPIO的
        self.pixels = neopixel.NeoPixel(machine.Pin(self.PIN),self.pixnumber)  # 创建一个Neopixel的对象。
        self.offcolor = backgroundcolor
 
    def showrandom(self): 
        print("    Enter random() ")
        for i in range(0,self.pixnumber):
            self.pixels[i] = (urandom.getrandbits(2),urandom.getrandbits(2),urandom.getrandbits(2))
        self.pixels.write()

    def clean(self):
        self.pixels.fill(self.offcolor)
        self.pixels.write()
  
    def off(self):
        self.pixels.fill((0,0,0))
        self.pixels.write()
        
    def nowtime(self):
        (year, month, mday, hour, minute, second,weekday,yearday)=time.localtime(time.time()+8*3600)
        return "{:0>2d}:{:0>2d}:{:0>2d}".format(hour, minute, second)

    # 定义写数字的函数，在指定坐标写0~9的数字，small是最小格式显示，使用5行，三列显示所有数字。

    def __small(self,displaynumber='8',xy=(0,0),color=(33,0,10)):
      x,y=xy
      #点阵字体的不亮点
      NUMBEROFF=[
             [4,7,10],[0,2,3,5,6,8,9,11,12,14],   # 0,1
             [3,4,10,11],[3,4,9,10],   # 2,3
             [1,4,9,10,12,13],[4,5,9,10],   # 4,5
             [4,5,10],[3,4,6,7,9,10,12,13],   # 6,7
             [4,10],[4,9,10]]   # 8,9
      for i in range(0,5):
          for j in range(0,3):
              onpoint=(i*3)+j
              if onpoint in NUMBEROFF[int(displaynumber)]:
                  self.pixels[self.XY[x+i][y+j]]=self.offcolor
              else:
                  self.pixels[self.XY[x+i][y+j]]=color

    ## 每5*7为一个显示单元

    def __large(self,displaynumber='8',xy=(0,0),color=(1,1,1)):
      x,y=xy
      #点阵字体的不亮点
      NUMBEROFF=[
             [0,4,6,7,8,11,12,16,18,22,23,26,27,28,30,34],[0,1,3,4,5,8,9,10,11,13,14,15,16,18,19,20,21,23,24,25,26,28,29,30,34],   # 0,1
             [0,4,6,7,8,10,11,12,13,15,19,21,22,23,24,26,27,28,29],[5,6,7,8,10,11,12,14,15,16,19,20,21,22,23,26,27,28,30,34],   # 2,3
             [0,1,2,4,5,6,9,10,12,14,16,17,19,25,26,27,29,30,31,32,34],[6,7,8,9,14,15,16,17,18,20,21,22,23,26,27,28,30,34],   # 4,5
             [0,1,5,7,8,9,11,12,13,14,19,21,22,23,26,27,28,30,34],[5,6,7,8,10,11,12,14,15,16,18,19,20,21,23,24,25,26,28,29,30,31,33,34],   # 6,7
             [0,4,6,7,8,11,12,13,15,19,21,22,23,26,27,28,30,34],[0,4,6,7,8,11,12,13,15,20,21,22,23,25,26,27,28,30,34]]   # 8,9
      if displaynumber == ':':
          self.pixels[self.XY[x+1][y]]=color;self.pixels[self.XY[x+1][y+1]]=color  #
          self.pixels[self.XY[x+2][y]]=color;self.pixels[self.XY[x+2][y+1]]=color  #
          self.pixels[self.XY[x+4][y]]=color;self.pixels[self.XY[x+4][y+1]]=color  #
          self.pixels[self.XY[x+5][y]]=color;self.pixels[self.XY[x+5][y+1]]=color  #
          return
      for i in range(0,7):
          for j in range(0,5):
              onpoint=(i*5)+j
              if onpoint in NUMBEROFF[int(displaynumber)]:
                  self.pixels[self.XY[x+i][y+j]]=self.offcolor
              else:   
                  self.pixels[self.XY[x+i][y+j]]=color

  
    def getlightcolor(self,index):
      lightvalue=readlight()
      #print("get the light value : %s" %(lightvalue))
      # colors=[(0,1,0),(0,1,0),(1,0,0),(0,1,0),(0,1,0),(1,0,1),(1,0,1)]  # 一共7个字符，每个字符显示的颜色。
      if lightvalue>0 and lightvalue<254:
        return tuple([i*lightvalue for i in self.colors[index]])
      
    def showtime_large(self,xy=(0,0),timestring='00:00:00'):
      print(timestring)
      x,y=xy   #显示坐标
      self.__large(timestring[0],(x,y),self.getlightcolor(0))
      self.__large(timestring[1],(x,y+6),self.getlightcolor(1))
      self.__large(':',(x,y+12),self.getlightcolor(2))
      self.__large(timestring[3],(x,y+15),self.getlightcolor(3))
      self.__large(timestring[4],(x,y+21),self.getlightcolor(4))
      self.__small(timestring[6],(x+2,y+26),self.getlightcolor(5))
      self.__small(timestring[7],(x+2,y+29),self.getlightcolor(6))
      self.pixels.write()
      time.sleep_ms(600)
      self.__large(':',(x,y+12),self.offcolor)
      self.pixels.write()
  
    def showtime(self):
      self.showtime_large(timestring=self.nowtime())


  
if __name__=='__main__':
  myneopixelpad=MyNeoPixelPad(23)
  myneopixelpad.clean()
  
  myneopixelpad.showtime()
  
  time.sleep(10)
  myneopixelpad.clean()
  myneopixelpad.showrandom()
  time.sleep(1)
  myneopixelpad.clean()








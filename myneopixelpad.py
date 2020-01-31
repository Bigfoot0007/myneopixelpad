# -*- coding: UTF-8 -*-
import machine, neopixel
import urandom
import time
import os
from light import *
import th

class MyNeoPixelPad:
    XY=[[i*8+j if (i%2==0) else i*8+(7-j) for i in range(32)] for j in range(8)]  # 使用了牛逼的list初始化算法。UNUNUNUN
    offcolor=(0,0,0)   # 关闭的颜色，或者背景颜色
    pixnumber=8*32  # pad size
    timecolors=[
              [(0,1,0),(0,1,0),(1,0,0),(0,1,0),(0,1,0),(1,0,1),(1,0,1)],  # 一共7个字符，每个字符显示的颜色。
              [(2,1,3),(2,1,3),(0,0,1),(2,1,3),(2,1,3),(1,0,1),(1,0,1)],  # 一共7个字符，每个字符显示的颜色。
              [(0,1,4),(0,1,4),(1,0,0),(0,1,4),(0,1,4),(1,0,1),(1,0,1)],  # 一共7个字符，每个字符显示的颜色。
              [(2,1,8),(2,1,8),(1,0,0),(2,1,8),(2,1,8),(6,1,1),(6,1,1)]]  # 一共7个字符，每个字符显示的颜色。
              
    thcolors=[
            [(0,1,0),(0,1,0),(0,1,0),(0,1,0),(0,0,1),(1,0,1),(1,0,1),(1,0,1),(1,0,1)],  # 一共9个字符，每个字符显示的颜色。
            [(12,12,12),(12,12,12),(12,12,12),(12,12,12),(24,0,1),(1,0,1),(1,0,12),(1,0,12),(1,0,12)]]  # 一共9个字符，每个字符显示的颜色。


    def __init__(self,PIN=13,backgroundcolor=(0,0,0)):
        print(" The Neopixel using %s"%PIN)
        self.PIN=PIN  # 对应的PIN，GPIO的
        self.pixels = neopixel.NeoPixel(machine.Pin(self.PIN),self.pixnumber)  # 创建一个Neopixel的对象。
        self.offcolor = backgroundcolor
        self.lightvalue=readlight()  # read ENV light
        self.showtimes = 0 # 记录显示的次数，用于时间和温湿度的隔
        self.cleanflag=""
        self.clickcount = 0 # 记录click的次数，每click一次，增加一个值。
        self.clean()
        self.showrandom()
        time.sleep_ms(100)
        self.clean()
 
    def showrandom(self): 
        # print("    Enter random() ")
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
      NUMBEROFF={'0':[4,7,10],'1':[0,2,3,5,6,8,9,11,12,14],'2':[3,4,10,11],'3':[3,4,9,10],'4':[1,4,9,10,12,13],'5':[4,5,9,10],'6':[4,5,10],'7':[3,4,6,7,9,10,12,13],'8':[4,10],'9':[4,9,10],':':[0,1,2,3,4,5,6,7,8,9,10,11,12,14],'c':[1,2,3,4,5,10,11]}   
      for i in range(0,5):
          for j in range(0,3):
              onpoint=(i*3)+j
              if onpoint in NUMBEROFF[displaynumber]:
                  self.pixels[self.XY[x+i][y+j]]=self.offcolor
              else:
                  self.pixels[self.XY[x+i][y+j]]=color

    ## 每5*7为一个显示单元

    def __large(self,displaynumber='8',xy=(0,0),color=(1,1,1)):
      x,y=xy
      width=5 ## 系统默认字体宽度为5.
      #点阵字体的不亮点
      NUMBEROFF={'0':[0,4,6,7,8,11,12,16,18,22,23,26,27,28,30,34],'1':[0,1,3,4,5,8,9,10,11,13,14,15,16,18,19,20,21,23,24,25,26,28,29,30,34],   # 0,1
             '2':[0,4,6,7,8,10,11,12,13,15,19,21,22,23,24,26,27,28,29],'3':[5,6,7,8,10,11,12,14,15,16,19,20,21,22,23,26,27,28,30,34],   # 2,3
             '4':[0,1,2,4,5,6,9,10,12,14,16,17,19,25,26,27,29,30,31,32,34],'5':[6,7,8,9,14,15,16,17,18,20,21,22,23,26,27,28,30,34],   # 4,5
             '6':[0,1,5,7,8,9,11,12,13,14,19,21,22,23,26,27,28,30,34],'7':[5,6,7,8,10,11,12,14,15,16,18,19,20,21,23,24,25,26,28,29,30,31,33,34],   # 6,7
             '8':[0,4,6,7,8,11,12,13,15,19,21,22,23,26,27,28,30,34],'9':[0,4,6,7,8,11,12,13,15,20,21,22,23,25,26,27,28,30,34],   # 8,9
             ':':[0,1,6,7,12,13],'c':[]}   # :,c
      fontwidth={'0':5,'1':5,'2':5,'3':5,'4':5,'5':5,'6':5,'7':5,'8':5,'9':5,'c':5,':':2}  # 系统默认为5，特殊字符需要特殊宽度，比如：需要2个即可。
      for i in range(0,7):
          width=fontwidth[displaynumber]
          for j in range(0,width):
              onpoint=(i*width)+j
              if onpoint in NUMBEROFF[displaynumber]:
                  self.pixels[self.XY[x+i][y+j]]=self.offcolor
              else:   
                  self.pixels[self.XY[x+i][y+j]]=color

  
    def getlightcolor(self,index):
      # colors=[(0,1,0),(0,1,0),(1,0,0),(0,1,0),(0,1,0),(1,0,1),(1,0,1)]  # 一共7个字符，每个字符显示的颜色。
      timecolorlen=len(self.timecolors)
      timecolorindex=self.clickcount % timecolorlen  # 或的那组颜色的坐标
      lightindex=int(self.lightvalue/10)
      # print(self.lightvalue,timecolorlen,timecolorindex,lightindex)
      return tuple([int(i*self.lightvalue) for i in self.timecolors[timecolorindex][index]])
        
    def getthlightcolor(self,index):
      thcolorlen=len(self.thcolors)
      thcolorindex=self.clickcount % thcolorlen  # 或的那组颜色的坐标
      lightindex=int(self.lightvalue/10)
      return tuple([int(i*self.lightvalue) for i in self.thcolors[thcolorindex][index]])
      
    def setlightcolor(self):
      self.lightvalue=readlight()   # only 1~10 will return 

        
    def showtime_large(self,xy=(0,0),timestring='00:00:00'):
      # print(timestring)
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

    # 显示温度和湿度
    def showth_small(self,xy=(1,0),thstring='00.0c00.0'):
      #print(thstring)
      x,y=xy   #显示坐标
      ########### Temperature
      self.__small(thstring[0],(x,y),self.getthlightcolor(0))
      self.__small(thstring[1],(x,y+4),self.getthlightcolor(1))
      self.__small(thstring[2],(x,y+7),self.getthlightcolor(2))  # .
      self.__small(thstring[3],(x,y+10),self.getthlightcolor(3))
      self.__small(thstring[4],(x,y+14),self.getthlightcolor(4))
      ############# Humidity
      self.__small(thstring[5],(x,y+18),self.getthlightcolor(5))
      self.__small(thstring[6],(x,y+22),self.getthlightcolor(6))
      self.__small(thstring[7],(x,y+25),self.getthlightcolor(7))  # .
      self.__small(thstring[8],(x,y+28),self.getthlightcolor(8))
      self.pixels.write()
      
    def showtime(self):
      self.setlightcolor()  # get env light
      if self.cleanflag != 'showtime':
        self.clean()
        self.cleanflag='showtime'
      # self.clean()
      self.showtime_large(timestring=self.nowtime())

    def showth(self):
      self.setlightcolor()  # get env light
      if self.cleanflag != 'showth':
        self.clean()
        self.cleanflag='showth'
      thstring="{:0>2.1f}c{:2.1f}".format(th.temperature(),th.humidity())
      self.showth_small(thstring=thstring.replace(".",":"))
      
    def showtimeandth(self):
      if self.showtimes % 5 == 0:
        self.showth()
      else:
        self.showtime()
      self.showtimes+=1
    
    def onclick(self):
      self.clickcount+=1
      print("on click :", self.clickcount)
  
if __name__=='__main__':
  myneopixelpad=MyNeoPixelPad(23)
  myneopixelpad.clean()
  
  myneopixelpad.showth()
  time.sleep(1)
  myneopixelpad.showtime()
  time.sleep(10)
  myneopixelpad.clean()
  myneopixelpad.showrandom()
  time.sleep(1)
  myneopixelpad.clean()













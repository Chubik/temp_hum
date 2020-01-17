#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import logging
import time
import traceback
import Adafruit_DHT
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)

RST = None
font_size = 15
num_line_len = 100      # X distance to hum and temp nummers 
max_temp = 60           # max processor temperature to warning
icon_size_cell = 20     # X distance to text

font = ImageFont.truetype('univers.ttf', font_size)
sensor = Adafruit_DHT.DHT11
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)



top = 0
x = 0

disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height

imageT = Image.open('temperature.bmp').convert('1')
imageH = Image.open('humidity2.bmp').convert('1')


def end():
    logging.info("Goto Sleep...")
    disp.reset()

def t_gpu():
        temp = os.popen("vcgencmd measure_temp").readline()
        temp=temp.replace("'C\n","")
        return (temp.replace("temp=",""))

try:
    hu, te = 0, 0
    while (1):
        image1 = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image1)
        humidity, temperature = Adafruit_DHT.read_retry(sensor, 4)
        t=t_gpu()
        if float(t) > max_temp:
            print ("proc temp: ", t, end="")
            draw.text((x, top), t,  font=font, fill=255)
            hu = 0

            disp.image(image1)
            disp.display()
            time.sleep(10)

        if hu != humidity or te != temperature:
            hu = humidity
            te = temperature
            t = str(te)
            h = str(hu)

            draw.text((x+icon_size_cell, top), "Temperature: ",  font=font, fill=255)
            draw.text((x+icon_size_cell, top+font_size), "Humidity: ",  font=font, fill=255)

            draw.text((x+num_line_len, top), t,  font=font, fill=255)
            draw.text((x+num_line_len, top+font_size), h,  font=font, fill=255)
            draw.bitmap((x,top),imageT, fill=255)
            draw.bitmap((x,top+2+font_size),imageH, fill=255)

            disp.image(image1)
            disp.display()
            
    image1.close()        
    time.sleep(5)
    end()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    end()
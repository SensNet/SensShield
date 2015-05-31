#!/usr/bin/env python
# -*- coding: utf-8 -*-
##requires PIL, Adafruit libs for SSD1306 and RPi.GPIO
import time
 
import Adafruit_SSD1306
import netifaces
import RPi.GPIO as GPIO
from Pages import *
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


FIXED = 7
LEFT = 10
RIGHT = 25
#Header (or in this case: footer...) anyway: Line with current page name and nav 
def drawHeader(header, draw, font, active):
	colors = [(128, 0), (128, 0)]
	if active == LEFT:
		colors[0] = (0, 128)
	if active == RIGHT:
		colors[1] = (0, 128)
	draw.rectangle(((0,height), (12, height-12)) , fill=colors[0][0])
	draw.rectangle(((width, height),(width-12,height-12)) , fill=colors[1][0])
	draw.text(((width - font.getsize(header)[0])/2, height-font.getsize(header)[1]), header, font=font, fill=255)
	draw.line(((0, height-12),(width, height-12)), fill=128)
	draw.polygon(((2,height-6),(10,height-2),(10,height-10)), fill=colors[0][1])
	draw.polygon(((width-2,height-6),(width-10,height-2), (width-10, height-10)), fill=colors[1][1])

#General "logics"
width = 0
height = 0
currentPage = 0;

def nextPage():
	global currentPage
	if currentPage == len(pages)-1:
		currentPage = 0;
		return
	currentPage += 1

def prevPage():
	global currentPage
	if currentPage == 0:
		currentPage = len(pages) -1
		return
	currentPage -= 1

lastLeft = 1
lastRight = 1
def drawLoop(disp, font):
	while 1:
		global lastLeft, lastRight
		image = Image.new('1', (width, height))
		draw = ImageDraw.Draw(image)
		active = 0;
		l = GPIO.input(LEFT)
		if l != lastLeft:
			if l == 0:
				active = LEFT
				prevPage()
			lastLeft = l;
		r = GPIO.input(RIGHT)
                if r != lastRight:
			if(r == 0):
				active = RIGHT
				nextPage()
			lastRight = r;
		p = pages[currentPage]
		drawHeader(p.getName(), draw, font, active)
		p.draw(draw, font)
		disp.image(image)
     		disp.display()
 
def main():
	global pages;
	font =  ImageFont.truetype("/root/oled/OpenSans-Regular.ttf", 11);
	disp = Adafruit_SSD1306.SSD1306_128_64(rst="", i2c_bus=2)
	disp.begin()
	disp.clear()
	disp.display()
	global width
	width  = disp.width
	global height
	height = disp.height
	pages = [NetworkPage(width, height), SystemPage(width, height)]
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(FIXED, GPIO.IN)
	GPIO.setup(LEFT, GPIO.IN)
	GPIO.setup(RIGHT, GPIO.IN)
	drawLoop(disp, font)


if __name__ == "__main__":
	main()


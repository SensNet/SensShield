# -*- coding: utf-8 -*-
from Page import Page
import netifaces
import psutil
import time
import RPi.GPIO as GPIO
import oled

class NetworkPage(Page):
	def getName(self):
		return "Network"

	def draw(self, draw, font):
        	inet = netifaces.AF_INET
        	top = 0;
        	ifaces = netifaces.interfaces()
        	for i in ifaces:
                	if i.startswith("lo"):
                        	continue
                	addr = netifaces.ifaddresses(i);
                	if inet in addr:
                        	addr = addr[inet][0]['addr']
                	else:
                        	addr = "-down-"

                	draw.text((0, top), i + ": " + addr, font=font, fill=255)
                	top += 11;

class SystemPage(Page):
	__lastgps = 0
	def getName(self):
                return "System"

        def draw(self, draw, font):
                if GPIO.input(oled.FIXED):
			self.__lastgps = time.time()
		top = 0
		with open ("/sys/devices/platform/sunxi-i2c.0/i2c-0/0-0034/temp1_input", "r") as myfile:
                        data=float(myfile.read())
                        data/=1000
			data=str(data)
                if data is None:
                        data = "n/a"
                draw.text((0,top), "Coretemp.: "+ data + "\xb0C", font=font, fill=256)
		top += 11;
		draw.text((0,top), "CPU Load: " + str(psutil.cpu_percent(interval=0))+"%", font=font, fill=256)
		top += 11
		gp = "Scanning..."
		if time.time()-self.__lastgps > 20:
			gp = "Ready"
		draw.text((0, top), "GPS: " + gp, font=font, fill=256)
		top += 14
		t = time.strftime("%Y-%m-%d %I:%M:%S")
		draw.text(((self.width-font.getsize(t)[0])/2,top), t, font=font, fill=256)

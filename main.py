#!/usr/bin/python

import smbus
import time
from logstash import send_event


bus = smbus.SMBus(1)

address = 0x43

def write(value):
	result = bus.write_byte_data(address, value & 0xff, (value & 0xff) >> 8)
	
	print result
	return -1

def write_block(cmd, value):
	result = bus.write_i2c_block_data(address, cmd & 0xff, value)
	print result

def read_block(cmd):
	return bus.read_i2c_block_data(address, cmd)


# Disable low power mode
write(0x10)
active = False 
while not active:
	active =  bus.read_byte_data(address, 0x11)

read_block(0x21)

write_block(0x21, [0x03])

read_block(0x21)

write_block(0x22, [0x03])

while True:
	write_block(0x22, [0x03])
	result = read_block(0x30)
	write_block(0x23, [0x03])
	rawTemp = ((result[1] << 8) | result[2])
	celcius = ((rawTemp / 64.0) - 273.15)
	fahrenheit = celcius * 9/5 + 32
	rawHumidity = ((result[4] << 8) | result[5])
	humidity = (rawHumidity / 512)
	data = {"temp": celcius, "humidity": humidity}
	send_event('office','weather', data)
	print 'Temp: {0} C, {1} F, Humidity {2}'.format(celcius, fahrenheit, humidity)
	time.sleep(60)

write_block(0x23, [0x03])
		


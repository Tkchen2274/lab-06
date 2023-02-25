#!/usr/bin/env python
#
# GrovePi Example for using the Grove Rotary Angle Sensor (Potentiometer) and the Grove LED to create LED sweep
#
# Modules:
#	 http://www.seeedstudio.com/wiki/Grove_-_Rotary_Angle_Sensor
#	 http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License
The MIT License (MIT)
GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import grovepi
from grove_rgb_lcd import*
from grovepi import*
import sys

textCommand(0x80 + 0x04)
bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, [0x48, 0x65, 0x6C, 0x6C, 0x6F])   # write "Hello"
time.sleep(3)
setText("Hello world \nLCD test")
setRGB(0,128,64)
# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0

# Connect the LED to digital port D5
# SIG,NC,VCC,GND
led = 5

grovepi.pinMode(potentiometer,"INPUT")
grovepi.pinMode(led,"OUTPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5
grovepi.set_bus("RPI_1")
# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
full_angle = 300
last_degree = 0
last_ultra = 0
ultrasonic_ranger = 4

setText("     cm\n" +"     cm")
#setText_norefresh("aa")
time.sleep(1)
first = True
while True:
    try:
        ultrrange = grovepi.ultrasonicRead(ultrasonic_ranger)
        # Read sensor value from potentiometer
        sensor_value = grovepi.analogRead(potentiometer)

        # Calculate voltage
        voltage = round((float)(sensor_value) * adc_ref / 1023, 1)

        # Calculate rotation in degrees (0 to 300)
        degrees = round((voltage * 250) / grove_vcc, 1)
        degrees = round(sensor_value / (1023/250) , 1)
        degrees = int(degrees)
        
        # degrees = round(sensor_value/3.4, 0)
        # Calculate LED brightess (0 to 255) from degrees (0 to 300)
        brightness = int(degrees / 250 * 255)
        if(degrees > 999):
            degrees = 999
        else: 
            text =degrees
        if(ultrrange > 999):
            ultrrange = 999
        else:
            text2 = ultrrange
        # Give PWM output to LED
        grovepi.analogWrite(led,brightness)
        
        if degrees < ultrrange:
            if(degrees != last_degree or ultrrange != last_ultra):
                textCommand(0x80 + 0x08)
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, [ord(' '), ord(' '), ord(' '), ord(' '), ord(' '), ord(' '), ord(' '), ord(' ')])
                text = str(text) 
                text2 = str(text2)
                textCommand(0x80 + 0x01)
                ascii_codes = [ord(c) for c in text]

                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, [ord(' '), ord(' '), ord(' ')])
                if len(ascii_codes) == 1:
                    textCommand(0x80 + 0x03)
                elif len(ascii_codes) == 2:
                    textCommand(0x80 + 0x02)
                else:
                    textCommand(0x80 + 0x01)
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, ascii_codes)
                #setText_norefresh(text)
                ascii_codes = [ord(c) for c in text2]
                
                textCommand(0xC0 +0x01)
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, [ord(' '), ord(' '), ord(' ')])
                if len(ascii_codes) == 1:
                    textCommand(0xC0 + 0x03)
                elif len(ascii_codes) == 2:
                    textCommand(0xC0 + 0x02)
                else:
                    textCommand(0xC0 + 0x01)
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, ascii_codes) 
                setRGB(0,255,0)
        else:
            if(degrees != last_degree or ultrrange != last_ultra):
                #setText_norefresh(str(degrees) + " cm OBJ PRES\n" + str(ultrrange) + " cm")
                setRGB(255,0,0)
                #bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x80,[ord(' '), ord(' '), ord(' ')])
                text = str(text) 
                text2 = str(text2)
            
                ascii_codes = [ord(c) for c in text]
                textCommand(0x80 + 0x01) 
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, [ord(' '), ord(' '), ord(' ')])
                if len(ascii_codes) == 1:
                    textCommand(0x80 + 0x03)
                elif len(ascii_codes) == 2:
                    textCommand(0x80 + 0x02)
                else:
                    textCommand(0x80 + 0x01)

                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, ascii_codes)

                #setText_norefresh(text)
                ascii_codes1 = [ord(c) for c in text2]
                
                textCommand(0xC0 +0x01)
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, [ord(' '), ord(' '), ord(' '), ord(' ')])
                print((ascii_codes))
                if len(ascii_codes1) == 1:
                    textCommand(0xC0 + 0x03)
                elif len(ascii_codes1) == 2:
                    textCommand(0xC0 + 0x02)
                else:
                    textCommand(0xC0 + 0x01)
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, ascii_codes1)  

                textCommand(0x80 + 0x08) #indicates first row @ column 0 and moves it 7 places
                text3 = "OBJ PRES"
                bus.write_i2c_block_data(DISPLAY_TEXT_ADDR, 0x40, [ord(c) for c in text3])
        
        last_degree = degrees
        last_ultra = ultrrange
        print("threshold_value = %d ultrasonic_vlue = %d" %(degrees,ultrrange))
        time.sleep(0.4)
        #print("sensor_value = %d voltage = %.2f degrees = %.1f brightness = %d" %(sensor_value, voltage, degrees, brightness))
    except KeyboardInterrupt:
        grovepi.analogWrite(led,0)
        break
    except IOError:
        print ("Error")

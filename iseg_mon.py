#!/usr/bin/python

import os, sys, time, termios , commands
try:
    import serial     
except Exception, e:
    print e
    sys.exit(1)

################################################################################ Global data
delay = 2
BAUDS = 9600
######################################################################## Platform-dependent port names
if sys.platform == "win32":
    DEVICE = 'COM8'
elif sys.platform.startswith("linux"):
    DEVICE = '/dev/ttyUSB0'   # '/dev/ttyS0' 
else:
    print "Warning: could not determine platform."
    print 'Please write the device name of the com1 port (windows = "com1", linux = "/dev/ttyS0")'
    DEVICE = raw_input("?")
################################################################### General: Intro, Open/close serial, Module Identifier, R/W break time
def Introduction():
    print "-"*117
    print "  Python program for controlling a module NIM ISEG 225 M - High Voltage Power Supply.                        "
    print "  (C) 2009 Author: Martin Gascon  -   University of Santiago de Compostela  - email: martin.gascon_usc.es  "
    print "-"*117 

def openSerial():    #opens the serial port
    global ser
    print "opening serial port... (%s, %d bps)\n" % (DEVICE, BAUDS),
    ser = serial.Serial(DEVICE, BAUDS, timeout=10)        
    ser.write("\r\n")
    ser.readline()
    ser.readline()
    print "ok."

def closeSerial():   #closes the port
    global ser
    print "closing serial port...", 
    if ser != None and ser.isOpen():
        ser.close()
    print "ok."




            

################################################################################# Main Menu

def Menu():         # Main Menu

    while 1:
            fileHandle = open ( 'Vmon.txt', 'a' )
            ser.write("U1\r\n")
            ser.readline()
            result =  ser.readline()
            time = commands.getoutput('date +%T')
	    cad = time+"  "+result
            print cad
            fileHandle.write(cad)

def main():
    try:
        openSerial()
    except:
        print "could not open serial port. Check that the device name "
        print "is correct (%s) and that the device is plugged to the connector" % DEVICE
        sys.exit(1) 
    
    Introduction()
    Menu()
    closeSerial()
    
            
if __name__ == "__main__":   # does not execute main if this module was imported
    main()


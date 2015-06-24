#!/usr/bin/env python
#Python script for reading data from Tektronix TDS scopes
#
#(C) 2007 David Perez Loureiro <dplourei@usc.es>
# this is distributed under a free software license
print ""
print "---------------------------------------------------------------------"
print "Program for serial interfacing with  Tektronix TDS2000 oscilloscopes "
print " D. Perez Loureiro GENP (USC) Setptember 2007"
print "---------------------------------------------------------------------"
print ""
n=input("Type the number of events you want to acquire: ")
import serial
signal=open('signal.dat','w')
header=open('header.dat','w')
#for Windows interfacing
#ser=serial.Serial('COM7', 19200, timeout=0.75)
#for Linux interfacing
ser=serial.Serial('/dev/ttyS0', 19200, timeout=0.75)
#Checks statur of SERIAL port
#ser.isOpen()
#identification of Scope
ser.write("id?\n")
s=ser.readline()
print s
#Selects acquisition mode
#ser.write("acq:mode sample;stopafter runstop\n")
ser.write("acq:mode sample;stopafter sequence\n")
#for ASCII output
#ser.write("dat:sou ch1;:dat:start 0;:dat:stop 2500;:dat:enc asci\n")
#for BINARY output
ser.write("dat:sou ch1;:dat:start 0;:dat:stop 2500;:dat:enc rib\n")
#Sets the waveform data point format to Y
ser.write("wfmp:pt_f y\n")
#Deactivates headers in commands
ser.write("head off\n")
#Query for the header information
ser.write("wfmpre?\n")
h=ser.readline()
header.write(h)
#print "header: %s"%h
#clears the device
ser.sendBreak()
x=ser.readline()
print "Entering LOOP"
#for i in range(0,n):
i=0
while i<n:
    #starts acquisition
    ser.write("acq:state run\n")
    #ser.write("trig:state?\n")
    #w=ser.readline()
    #print ""
    #print w
    #ser.write("wavf?\n")
    ser.write("trig:state?\n")
    w=ser.readline()
    if (w=='SAV' or w=='SAV\n'or w=="SAV\r"):
        ser.write("*WAI\n")
        #Gets the waveform without header
        ser.write("curve?\n")
        s=ser.readline()
        print "SIGNAL %d"%(i+1)
        #print s
        i=i+1
        signal.write(s)
    else:
        #i=i-1
        print "NO TRIGGER"
        #print i 
         #ser.write("*CLS\n")
        ser.sendBreak()
        c=ser.readline()
        #print w
        continue
    #ser.write("trig:state?\n")
    #h=ser.readline()
    #print "Estoy aqui"
    #print h
    #ser.write("acq:state stop\n")
    #ser.sendBreak()
    #q=ser.readline()
    #print q
    #file.write("\n\n 0xdeadface\n\n")
signal.close()
header.close()
#ser.close()
#w=ser.isOpen()
#print w
print "DONE!!!!!!!!!!!"

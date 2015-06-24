#!/usr/bin/env python
#Python script for reading data from Tektronix TDS scopes
#
#(C) 2007 David Perez Loureiro <dplourei@usc.es>
# this is distributed under a free software license, see license.txt
print ""
print "-----------------------------------------------------------------"
print "Program for serial interfacing with  Tektronix TDS oscilloscopes "
print "-----------------------------------------------------------------"
print ""
n=input("Type the number of events you want to acquire: ")
import serial
signal=open('signal.dat','w')
header=open('header.dat','w')
#for Windows interfacing
#ser=serial.Serial('COM7', 19200, timeout=10)
#for Linux interfacing
ser=serial.Serial('/dev/ttyS0', 19200, timeout=0.5)
#ser.isOpen()
ser.write("id?\n")
s=ser.readline()
#print ""
print s
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
#checks status of the trigger
ser.write("trig:state?\n")
w=ser.readline()
#print ""
print w
#Query for the header information
ser.write("wfmpre?\n")
h=ser.readline()
header.write(h)
#print "header: %s"%h
#clears the device
ser.sendBreak()
print "Entering LOOP"
for i in range(0,n):
    ser.sendBreak()
    print "SIGNAL %d"%(i+1)
    #stops acquisition
    ser.write("acq:state stop\n")
    #starts acquisition
    ser.write("acq:state run\n")
    ser.write("trig:state?\n")
    h=ser.readline()
    print h
    #ser.write("wavf?\n")
    #Gets the waveform without header
    ser.write("curve?\n")
    s=ser.readline()
    #writes signal to file
    signal.write(s)
    ser.write("*CLS\n")
    #ser.sendBreak()
    #prints signal
    print s
    ser.write("*OPC?\n")
    w=ser.readline()
    #print w
    ser.write("acq:state stop\n")
    ser.sendBreak()
#Closes files    
signal.close()
header.close()
#Close port
ser.close()
#w=ser.isOpen()
#print w

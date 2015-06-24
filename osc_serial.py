#!/usr/bin/env python
#Python script for reading data from Tektronix TDS scopes
#
#(C) 2006 David Perez Loureiro <dplourei@usc.es>
# this is distributed under a free software license, see license.txt
print ""
print "-----------------------------------------------------------------"
print "Program for serial interfacing with  Tektronix TDS oscilloscopes "
print "-----------------------------------------------------------------"
print ""
#n=input("Type the number of events you want to acquire: ")
import serial
signal=open('signal.dat','w')
#header=open('header.dat','w')
#for Windows interfacing
#ser=serial.Serial('COM7', 19200, timeout=10)
#for Linux interfacing
ser=serial.Serial('/dev/ttyS0', 9600, timeout=1)
#ser=serial.Serial('/dev/ttyS2', 19200, timeout=10)
ser.isOpen()
ser.write("id?\n")
s=ser.readline()
print ""
print s
ser.write("trig:state?\n")
s=ser.readline()
print ""
print s
ser.write("acq:state 0\n")
ser.write("acq:mode sample;stopafter sequence\n")
#ser.write("acq:mode sample;stopafter runstop\n")
ser.write("acq:state 1\n")
#ser.write("dat:sou ch1;:dat:start 0;:dat:stop 2500;:dat:enc asci\n")
ser.write("dat:sou ch1;:dat:start 0;:dat:stop 2500;:dat:enc rib\n")
ser.write("wfmp:pt_f y\n")
#ser.write("wavf?\n")
ser.write("trig:state?\n")
s=ser.readline()
print ""
print s
ser.write("curve?\n")
s=ser.readline()
print ""
print s
ser.write("trig:state?\n")
s=ser.readline()
print ""
print s
ser.write("acq:numac?\n")
s=ser.readline()
print s
ser.write("acq:state 0\n")
#ser.write("*cls\n")
ser.write("acq:state 1\n")
ser.write("trig:state?\n")
s=ser.readline()
print ""
print s
ser.write("curve?\n")
s=ser.readline()
signal.write(s)
print ""
print s
ser.write("trig:state?\n")
s=ser.readline()
print ""
print s
ser.write("acq:state 0\n")
#ser.close()

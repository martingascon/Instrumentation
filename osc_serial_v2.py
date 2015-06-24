#!/usr/bin/env python
#Python script for reading data from Tektronix TDS scopes
#
#(C) 2006 David Perez Loureiro <dplourei@usc.es>
# this is distributed under a free software license
#------------------------------------------------------
# History:
#
#Jun 06:  New commands added for only trigger acq. 
#------------------------------------------------------
print ""
print "-----------------------------------------------------------------"
print "Program for serial interfacing with  Tektronix TDS oscilloscopes "
print "-----------------------------------------------------------------"
print ""
n=input("Type the number of events you want to acquire: ")
import serial
file=open('signal.dat','w')
ser=serial.Serial('/dev/ttyS0', 9600, timeout=10)
#ser.isOpen()
ser.write("acq:mode sample;stopafter sequence\n")
#ser.write("acq:mode sample;stopafter runstop\n")
ser.write("acq:state 1\n")
ser.write("dat:sou ch1;:dat:start 0;:dat:stop 2500;:dat:enc asci\n")
#ser.write("dat:sou ch1;:dat:start 0;:dat:stop 2500;:dat:enc rib\n")
ser.write("wfmp:pt_f y\n")
ser.write("id?\n")
s=ser.readline()
print ""
print s
for i in range(0,n):
    ser.write("acq:numac?\n")
    ser.readline()
    #ser.write("wavf?\n")
    ser.write("curve?\n")
    s=ser.readline()
    #print ""
    print i
    #file.write("%d \n"% i)
    file.write(s)
    #file.write("\n\n 0xdeadface\n\n")
file.close()


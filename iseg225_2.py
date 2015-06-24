#!/usr/bin/python

import os, sys, time, termios, commands

try:
    import serial     
except Exception, e:
    print e
    sys.exit(1)

################################################################################ Global data
delay = 0.1
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
    result =  ser.readline()
    result =  ser.readline()
    print result
    print "ok."

def closeSerial():   #closes the port
    global ser
    print "closing serial port...", 
    if ser != None and ser.isOpen():
        ser.close()
    print "ok."


def whichChan(prompt): # channel 
    while 1:
       chan = raw_input(prompt)
       if chan == "a":
           return chan
       elif chan == "b":
           return chan
       else:
           print "wrong channel"

def result():   # read the output for reading
    #time.sleep(delay)
    ser.readline()
    result =  ser.readline()
    print result[0]

def result2():   # read the output for writing
    result =  ser.readline()
    print result
    ser.readline()
    ser.readline()
  
############################################################################################ functions mid, rbt, wbt
def mid():  # Module Identifier (unit number ; software rel. ; Vout max ; Iout max )
    #ser.write("\r\n")
    ser.write("#\r\n")
    ser.readline()
    result =  ser.readline()   
    print "Unit number: %s "% (result[0:6])
    print "Software version.: %s "% (result[7:11])
    print "Iout max = %s "% (result[12:17])
    print "Vout max = %s" % (result[18:21])

def rbt():  #Read break time (0-255 ms),    ser.write("W\r\n")
    ser.readline()
    result =  ser.readline()

def wbt(time):  # Write break time (0-255 ms)
    ser.write("W=%d\r\n\r\n"%(time))
    result2()    
    print " ms"
#################################################################################   R/W Volt, I, limit, 
def readVolt(channel):  # Read actual voltage     if channel== "a":
        ser.write("U1\r\n")
        ser.readline()
        result =  ser.readline()        
	print "HV = %s.%s V" %(result[1:5],result[5:6])
    elif channel == "b":
	ser.write("U2\r\n")
        result()     
	return result       

def readCurr(channel):  # Read actual current    if channel== "a":
        ser.write("I1\r\n")
        result() 
    elif channel == "b":
	ser.write("I2\r\n")
        result()            

def voltLimit(channel):  # Read voltage limit    if channel== "a":
        ser.write("M1\r\n")
        result() 
    elif channel == "b":
	ser.write("M2\r\n")
        result()            

def currLimit(channel):  # Read current limit     if channel== "a":
        ser.write("N1\r\n")
        result() 
    elif channel == "b":
	ser.write("N2\r\n")
        result()            


def readSetVolt(channel):  # Read voltage limit    if channel== "a":
        ser.write("D1\r\n")
        result() 
    elif channel == "b":
	ser.write("D2\r\n")
        result()            

def writeSetVolt(channel,volt):  # Read current limit     if channel== "a":
        ser.write("D1=%d\r\n"%(volt))
        result2() 
    elif channel == "b":
	ser.write("D2=%d\r\n"%(volt)) 
        result2()          


def readRampSpeed(channel):  # read the ramp speed    if channel== "a":
        ser.write("V1\r\n")
        result() 
    elif channel == "b":
	ser.write("V2\r\n")
        result()            

def writeRampSpeed(channel,rs):  # Write the ramp speed     if channel== "a":
        ser.write("V1=%d\r\n\r\n"%(rs))
        result2() 
    elif channel == "b":
	ser.write("V2=%d\r\n\r\n"%(volt)) 
        result2()   


def startVolt(channel):  # start voltage change    if channel== "a":
        ser.write("G1\r\n")
        result() 
    elif channel == "b":
	ser.write("G2\r\n")
        result()    

def status(channel):  # read status word    if channel== "a":
        ser.write("S1\r\n")
        result() 
    elif channel == "b":
	ser.write("S2\r\n")
        result()   


def readCurrTrip(channel):  # read current trip    if channel== "a":
        ser.write("L1\r\n")
        result() 
    elif channel == "b":
	ser.write("L2\r\n")
        result()            

def writeCurrTrip(channel,curr):  # Write current trip    if channel== "a":
        ser.write("L1=%d\r\n\r\n"%(curr))
        result2() 
    elif channel == "b":
	ser.write("L2=%d\r\n\r\n"%(curr)) 
        result2()   

def statusMod(channel):  # read status module    if channel== "a":
        ser.write("T1\r\n")
        result() 
    elif channel == "b":
	ser.write("T2\r\n")
        result()     

def readAutoStart(channel):  # read auto start    if channel== "a":
        ser.write("A1\r\n")
        result() 
    elif channel == "b":
	ser.write("A2\r\n")
        result()            

def writeAutoStart(channel,cond):  # Write auto start    if channel== "a":
        ser.write("A1=%d\r\n\r\n"%(cond))
        result2() 
    elif channel == "b":
	ser.write("A2=%d\r\n\r\n"%(cond)) 
        result2()   





#################################################################################   HASTA ACA PERFECTO.

def getchar():
	fd = sys.stdin.fileno()
	if os.isatty(fd):
		old = termios.tcgetattr(fd)
		new = termios.tcgetattr(fd)
		new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
		new[6] [termios.VMIN] = 1
		new[6] [termios.VTIME] = 0
		try:
			termios.tcsetattr(fd, termios.TCSANOW, new)
			termios.tcsendbreak(fd,0)
			ch = os.read(fd,7)

		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, old)
	else:
		ch = os.read(fd,7)
	
	return(ch)


################################################################################# Read Options, Load, Save Files 

def readYN(prompt): # Yes or Not read function
    while 1:
       a = raw_input(prompt).lower().strip()
       if a == "y":
           return True
       elif a == "f":
           return False
           
def readInteger(prompt): #   reads user input until the entry is a valid integer
    while 1:
        a = raw_input(prompt)
        try:            return int(a)
        except:         print "  Provide an integer"
            

################################################################################# Main Menu

def Menu():         # Main Menu

    while 1:
        try:
            print "Press any key to continue ..."
            getchar() 
	    os.system('clear')    
	    Introduction()    
            print "-"*117
            print "|                                        GENERAL FUNCTIONS                                                          |"
  	    print "-"*117
            print "| id) Read module identifier: (unit No; software rel; Vout max; Iout max)                                           |" 
            print "| r) Read break time                                                               w) Write break time (0-255 ms)   |"
            print "-"*117
            print "|                                        CHANNEL FUNCTIONS                                                          |"
  	    print "-"*117
            print "| u) Read actual voltage     i) Read actual current        m) Read voltage limit      n) Read current limit         |"
            print "| d) Read set voltage        dn) Write set voltage         v) Read ramp speed         vn) Write ramp speed          |"
	    print "| g) Start voltage change    s) status information         l) Read current trip       ln) Write current trip        |"
	    print "| t) Read module status      a) Read auto start            an) Write auto start                                     |"

            print "-"*117
            print "|                                        EXTRA FUNCTIONS                                                            |"
            print "-"*117
            print "| vmon)  Monitorize the voltage (file record)     								     |"
   	    print "| x) EXIT        			    						                             |"
            print "-"*117         
	    print " "
                
            option = raw_input(" OPTION ? :  ") 
	    options = set(['u','i','m','n','d','dn','v','vn','g','s','l','ln','t','a','an','vmon'])
	    if option in options:
		channel = whichChan("Channel? : ")
###################################################################### general options       
            if option == "id":
                 mid()
            elif option == "r":
                 rbt()
            elif option == "w":
                 tim = readInteger("time? (0-255 ms): " )
                 wbt(tim)
            elif option == "vmon":
                 fileHandle = open ( 'Vmon.txt', 'a' )
            	 interval = input(" Interval ? (2 s - 600 s) :  ") 		
		 inte = float(interval)
                 while 1:
                 	result = readVolt(channel)
            	 	times = commands.getoutput('date +%T')
	    	  	cad = times + "  " + str(result)
            	   	print('\033[29;0H%s'%(cad))
            		fileHandle.write(cad)
			time.sleep(inte)
            elif option == "x":
                break
###################################################################### channel options    
            elif option == "u":
                readVolt(channel)            elif option == "i":
                readCurr(channel)            elif option == "m":
                voltLimit(channel)            elif option == "n":
                currLimit(channel)
            elif option == "d":
                readSetVolt(channel)            elif option == "dn":
                volt = raw_input(" Voltage ? (<m):  ") 
                writeSetVolt(channel,volt)
            elif option == "v":
                readRampSpeed(channel)            elif option == "vn":
                rs = raw_input(" Ramp Speed ? (2 - 255 V/s):  ") 
                writeRampSpeed(channel,rs)
            elif option == "g":
                startVolt(channel)
            elif option == "s":
                status(channel)
            elif option == "l":
                readCurrTrip(channel)            elif option == "ln":
                curr = raw_input(" Current? (<m):  ") 
                writeCurrTrip(channel,curr)
            elif option == "t":
                statusMod(channel)
            elif option == "a":
                readAutoStart(channel)            elif option == "an":
                cond = raw_input(" Conditions ?:  ") 
                writeAutoStart(channel,cond)
            else:
                print "wrong option"
                
        except KeyboardInterrupt:
            print
            print 
            print "<interrupted by user>"
            
        except:
            raise
            print "ERROR!"

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


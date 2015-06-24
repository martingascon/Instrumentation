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
    DEVICE = '/dev/ttyUSB2'   
else:
    print "Warning: could not determine platform."
    print 'Please write the device name of the COM port (windows = "COM4, COM5 ..", linux = "/dev/ttyUSB1, USB2 ...")'
    DEVICE = raw_input("?")
################################################################### General: Intro, Open/close serial, Module Identifier, R/W break time
def Introduction():
    print "-"*117
    print "  Python program for controlling a module NIM ISEG 225 M - High Voltage Power Supply.                        "
    print "  (C) 2009 Author: Martin Gascon  -   University of Santiago de Compostela  - email: martin.gascon_usc.es  "
    print "-"*117 

def openSerial():    #opens the serial port
    global ser
    print "Opening serial port... (%s, %d bps)\n" % (DEVICE, BAUDS),
    ser = serial.Serial(DEVICE, BAUDS, timeout=10)        
    ser.write("\r\n")    #In order to assure synchronisation between the computer and the supply
    ser.readline()
    ser.readline()  
    print " ... ok."

def closeSerial():   #closes the port
    global ser
    print "Closing serial port...", 
    if ser != None and ser.isOpen():
        ser.close()
    print " ... ok."


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
    ser.readline()
    result =  ser.readline()
    print result

def result2():   # read the output for writing
    result =  ser.readline()
    print result
    ser.readline()
    ser.readline()
  

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
    print "break time = %s ms"% (result[0:3])

def wbt(time):  # Write break time (0-255 ms)
    ser.write("W=%d\r\n\r\n"%(time))    
    result =  ser.readline()
    print "break time = %s ms"% (result[2:5])
    print "wait ..."
    ser.readline()
    ser.readline()

#################################################################################   R/W Volt, I, limit, 
def readVolt(channel):  # Read actual voltage     if channel== "a":
        ser.write("U1\r\n")
        ser.readline()
        result =  ser.readline()        
	print "HV = %s.%s V" %(result[1:5],result[5:6])
    elif channel == "b":
	ser.write("U2\r\n")
        ser.readline()
        result =  ser.readline()        
	print "HV = %s.%s V" %(result[1:5],result[5:6])  

def readCurr(channel):  # Read actual current    if channel== "a":
        ser.write("I1\r\n")
        ser.readline()
        result =  ser.readline()
	print "I = %s.%s uA" %(result[0:4],result[4:5])
    elif channel == "b":
	ser.write("I2\r\n")
        ser.readline()
        result =  ser.readline()
	print "I = %s.%s uA" %(result[0:4],result[4:5])

def voltLimit(channel):  # Read voltage limit    if channel== "a":
        ser.write("M1\r\n")
        ser.readline()
        result =  ser.readline()
	print "Volt. limit = %s %% " %(result[0:3])       

    elif channel == "b":
	ser.write("M2\r\n")
        ser.readline()
        result =  ser.readline()
	print "Volt. limit = %s %% " %(result[0:3])       

def currLimit(channel):  # Read current limit     if channel== "a":
        ser.write("N1\r\n")
        ser.readline()
        result =  ser.readline()
	print "Curr. limit = %s %% " %(result[0:3])       
    elif channel == "b":
	ser.write("N2\r\n")
        ser.readline()
        result =  ser.readline()
	print "Curr. limit = %s %% " %(result[0:3])

def readSetVolt(channel):  # Read voltage limit    if channel== "a":
        ser.write("D1\r\n")
        ser.readline()
        result =  ser.readline()        
	print "HV = %s.%s V" %(result[0:4],result[4:5])   
    elif channel == "b":
	ser.write("D2\r\n")
        ser.readline()
        result =  ser.readline()        
	print "HV = %s.%s V" %(result[0:4],result[4:5])   

def writeSetVolt(channel):  # Read current limit     volt = readInteger(" Voltage ? (<5000 V): ")
    if channel== "a":
        ser.write("D1=%d\r\n\r\n"%(volt))
        result =  ser.readline()
        print result
        ser.readline()
        ser.readline() 
    elif channel == "b":
	ser.write("D2=%d\r\n\r\n"%(volt)) 
        result =  ser.readline()
        print result
        ser.readline()
        ser.readline()           

def readRampSpeed(channel):  # read the ramp speed    if channel== "a":
        ser.write("V1\r\n")
        ser.readline()
        result =  ser.readline()        
	print "RS = %s V/s" %(result[0:3])   
    elif channel == "b":
	ser.write("V2\r\n")
        ser.readline()
        result =  ser.readline()        
	print "RS = %s V/s" %(result[0:3])   

def writeRampSpeed(channel):  # Write the ramp speed 
    rs = readInteger(" Ramp Speed ? (2 - 255 V/s):  ") 
    if channel== "a":
        ser.write("V1=%d\r\n\r\n"%(rs))
        result =  ser.readline()
        print result
        ser.readline()
        ser.readline()
    elif channel == "b":
	ser.write("V2=%d\r\n\r\n"%(volt)) 
        result =  ser.readline()
        print result
        ser.readline()
        ser.readline()


def startVolt(channel):  # start voltage change    if channel== "a":
        ser.write("G1\r\n")
        result =  ser.readline()
        print result
        ser.readline()
        ser.readline()
    elif channel == "b":
	ser.write("G2\r\n")
        result =  ser.readline()
        print result
        ser.readline()
        ser.readline()  

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
        ser.readline()
        result =  ser.readline()
        print result + " (code 0...255, => Module status) "
    elif channel == "b":
	ser.write("T2\r\n")
        ser.readline()
        result =  ser.readline()
        print result + " (code 0...255, => Module status) "
                                     


def readAutoStart(channel):  # read auto start    if channel== "a":
        ser.write("A1\r\n")
        ser.readline()
    	result =  ser.readline()
    	print result + " (8 => auto start is active; 0 => inactive)"
    elif channel == "b":
	ser.write("A2\r\n")
        ser.readline()
    	result =  ser.readline()
    	print result + " (8 => auto start is active; 0 => inactive)"      

def writeAutoStart(channel,cond):  # Write auto start    if channel== "a":
        ser.write("A1=%d\r\n\r\n"%(cond))
        result2() 
    elif channel == "b":
	ser.write("A2=%d\r\n\r\n"%(cond)) 
        result2()   


#################################################################################   Monitoring functions HV, I

def voltMon():  # Monitorizar el voltaje
    interval = input(" Interval ? (3 s - 6000 s) :  ") 		
    inte = float(interval)
    while 1:
        ser.write("U1\r\n")
        ser.readline()
        hv1 =  ser.readline()   
	V1= " %s.%s V" %(hv1[1:5],hv1[5:6])
	ser.write("U2\r\n")
        ser.readline()
        hv2 =  ser.readline() 
        V2= " %s.%s V" %(hv2[1:5],hv2[5:6]) 
        times = commands.getoutput('date +%T')
        cad = times + "  " + V1 + " " + V2
	print('\033[41;0H  Time       HV 1      HV 2')            	   	
	print('\033[42;0H%s'%(cad))
	time.sleep(inte-1)

def voltRecMon():  # Monitorizar el voltaje
    fileHandle = open ( 'HVmon.txt', 'a' )
    interval = input(" Interval ? (3 s - 600 s) :  ") 		
    inte = float(interval)
    while 1:
        ser.write("U1\r\n")
        ser.readline()
        hv1 =  ser.readline()   
	V1= " %s.%s V" %(hv1[1:5],hv1[5:6])
	ser.write("U2\r\n")
        ser.readline()
        hv2 =  ser.readline() 
        V2= " %s.%s V" %(hv2[1:5],hv2[5:6]) 
        times = commands.getoutput('date +%T')
        cad = times + "  " + V1 + " " + V2 + "\n"
	print('\033[41;0H  Time       HV 1       HV 2')    	  	   	
	print('\033[42;0H%s'%(cad))
        fileHandle.write(cad)
	time.sleep(inte-1)

def voltCurrMon():  # Monitorizar el voltaje
    interval = input(" Interval ? (3 s - 600 s) :  ") 		
    inte = float(interval)
    while 1:
        ser.write("U1\r\n")
        ser.readline()
        hv1 =  ser.readline()   
	V1= " %s.%s V" %(hv1[1:5],hv1[5:6])
	ser.write("U2\r\n")
        ser.readline()
        hv2 =  ser.readline() 
        V2= " %s.%s V" %(hv2[1:5],hv2[5:6]) 
        ser.write("I1\r\n")
        ser.readline()
        hv1 =  ser.readline()   
	I1= " %s.%s uA" %(hv1[0:4],hv1[4:5])
	ser.write("I2\r\n")
        ser.readline()
        hv2 =  ser.readline() 
        I2= " %s.%s uA" %(hv2[0:4],hv2[4:5]) 
        times = commands.getoutput('date +%T')
        cad = times + "  " + V1 + " " + V2 + "  " + I1 + " " + I2 
	print('\033[41;0H  Time       HV 1      HV 2        I1         I2')            	   	
	print('\033[42;0H%s'%(cad))
	time.sleep(inte-1)

def voltCurrRecMon():  # Monitorizar el voltaje
    fileHandle = open ( 'HVmon.txt', 'a' )
    interval = input(" Interval ? (3 s - 600 s) :  ") 		
    inte = float(interval)
    while 1:
        ser.write("U1\r\n")
        ser.readline()
        hv1 =  ser.readline()   
	V1= " %s.%s V" %(hv1[1:5],hv1[5:6])
	ser.write("U2\r\n")
        ser.readline()
        hv2 =  ser.readline() 
        V2= " %s.%s V" %(hv2[1:5],hv2[5:6]) 
        ser.write("I1\r\n")
        ser.readline()
        hv1 =  ser.readline()   
	I1= " %s.%s uA" %(hv1[0:4],hv1[4:5])
	ser.write("I2\r\n")
        ser.readline()
        hv2 =  ser.readline() 
        I2= " %s.%s uA" %(hv2[0:4],hv2[4:5]) 
        times = commands.getoutput('date +%T')
        cad = times + "  " + V1 + " " + V2 + "  " + I1 + " " + I2 +"\n"
	print('\033[41;0H  Time       HV 1      HV 2        I1         I2')            	   	
	print('\033[42;0H%s'%(cad))
        fileHandle.write(cad)
	time.sleep(inte-1)
#################################################################################   extra fucntions: getchar()

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
            print "|                                                 GENERAL FUNCTIONS                                                 |"
  	    print "-"*117
            print "| id) Read module identifier: (unit No; software rel; Vout max; Iout max)                                           |" 
            print "| r) Read break time                                                               w) Write break time (0-255 ms)   |"
            print "-"*117
            print "|                                                 CHANNEL FUNCTIONS                                                 |"
  	    print "-"*117
            print "| u) Read actual voltage     i) Read actual current        m) Read voltage limit      n) Read current limit         |"
            print "| d) Read set voltage        dn) Write set voltage         v) Read ramp speed         vn) Write ramp speed          |"
	    print "| g) Start voltage change    s) status information         l) Read current trip       ln) Write current trip        |"
	    print "| t) Read module status      a) Read auto start            an) Write auto start                                     |"
            print "-"*117
            print "|                                                   EXTRA FUNCTIONS                                                 |"
            print "-"*117
            print "| vmon) HV  Monitor (ch a and b)                             rvmon) HV Monitor (file record)  (ch a and b)          |"
            print "| vimon) HV and I Monitor (ch a and b)                       rvimon) HV and I Monitor (file record)  (ch a and b)   |"
   	    print "| x) EXIT        			    						                            |"
            print "-"*117         
	    print "|                                                  STATUS INFORMATION                                               |"
            print "-"*117
            print "|  ON<SP> Output voltage according to set voltage            MAN    Channel is on, set to manual mode               |"
            print "|  OFF    Channel front panel switch off                     ERR    Vmax or Imax is / was been exceeded             |"
            print "|  INH    Inhibit signal was been / is active                QUA    Quality of output voltage not given at present  |"
            print "|  L2H    Output voltage increasing                          H2L    Output voltage falling                          |"
            print "|  LAS    Look at Status (only after G-command)              TRP    Current trip was been active                    |"

            print "-"*117         
	    print "|                                                    ERROR CODES                                                    |"
            print "-"*117
            print "|  ???? Syntax error                                         ?WCN   Wrong channel number                            |"
            print "|  ?TOT  Timeout error (with following reinitialization)     ?<SP>UMAX=nnnn  Set voltage exceeds voltage limit      |"
            print "-"*117         
	    print " "
            option = raw_input(" OPTION ? :  ") 
	    options = set(['u','i','m','n','d','dn','v','vn','g','s','l','ln','t','a','an'])
	    if option in options:
		channel = whichChan(" Channel? : ")
###################################################################### general options       
            if option == "id":
                 mid()
            elif option == "r":
                 rbt()
            elif option == "w":
                 tim = readInteger("time? (0-255 ms): " )
                 wbt(tim)
            elif option == "vmon":
            	 voltMon()
            elif option == "rvmon":
            	 voltRecMon()
            elif option == "vimon":
            	 voltCurrMon()
            elif option == "rvimon":
            	 voltCurrRecMon()
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
               writeSetVolt(channel)
            elif option == "v":
                readRampSpeed(channel)            elif option == "vn":
                writeRampSpeed(channel)
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
        print "Could not open serial port. Check if the device is plugged correctly"
        sys.exit(1) 
    Menu()
    closeSerial()
    
            
if __name__ == "__main__":   # does not execute main if this module was imported
    main()


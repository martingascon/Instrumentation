#!/usr/bin/python

import os, sys, time
try:
    import serial     
except Exception, e:
    print e
    sys.exit(1)

#------- global data ---------
delay = 0.1
bus = 0
BAUDS = 9600
#-------------------------------
# solve platform-dependent port names
if sys.platform == "win32":
    DEVICE = 'COM8'
    
elif sys.platform.startswith("linux"):
    DEVICE = '/dev/ttyUSB1'   # '/dev/ttyS0' 
else:
    print "Warning: could not determine platform."
    print 'Please write the device name of the com1 port (windows = "com1", linux = "/dev/ttyS0")'
    DEVICE = raw_input("?")
################################################################################# General: On,Off, serial, Baudrate
def Introduction():
    print "-"*90
    print "  Mesytec MSCF-16. Spectroscopic Amplifier. University of Santiago de Compostela.          "
    print "  (C) 2009 Author: Martin Gascon                  email: martin.gascon_usc.es              "
    print "-"*90 
def SetRC_On():  # Switch RC mode on
    global bus
    ser.write("ON\r")
    s=ser.readlines()
    print s

    #time.sleep(delay)
    #result =  ser.read(ser.inWaiting())
    #print result
def SetRC_Off(): # Switch RC mode off
    global bus
    ser.write("OFF\r")
    s=ser.readlines()
    print s
    #time.sleep(delay)
    #result =  ser.read(ser.inWaiting())
    #print result

def openSerial():    #opens the serial port
    global ser
    print "opening serial port... (%s, %d bps)\n" % (DEVICE, BAUDS),
    ser = serial.Serial(DEVICE, BAUDS, timeout=10)        
    print "ok."
    
    
def closeSerial():   #closes the port
    global ser
    print "closing serial port...", 
    if ser != None and ser.isOpen():
        ser.close()
    print "ok."

def SetBaudrate(n):  # Set Baudrate to: n
    global bus
    ser.write("SB %d\r" %(n))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result

################################################################################# Gains, Thresholds, PZ, Shap.  HASTA ACa PERFECTO.
def SetGain(group,gain):  # Set Gain for groups of 4 channels       #if group == "0": group=5
    global bus
    ser.write("SG %d %d\r" %(group,gain))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result 
def SetThreshold(chan,thres):  # Set threshold value
    global bus
    ser.write("ST %d %d\r" %(chan, thres))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result 
def SetPoloZero(chan,pz):  # Set pz value
    global bus
    ser.write("SP %d %d\r" %(chan, pz))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result
def SetShaping(group,shap):  # Set shaping time for a group
    if group == "0": group=5
    global bus
    ser.write("SS %d %d\r" %(group, gain))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result 
def SetMult(high,low):  # Set multiplicity borders
    global bus
    ser.write("SM %d %d\r" %(high, low))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result     
def MonChan(chan):  # Set monitor output to channel
    global bus
    ser.write("MC %d\r" %(chan))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result
def SingleMode(mode):  # Single channel mode
    global bus
    ser.write("SI %d\r" %(mode))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result
def AutoPZ():  # Switch automatic pz setting on/off
    global bus
    ser.write("AP")
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    print result

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
            
    
def readFileName(prompt, mode):   
    """
    gets a valid file name.
    
    'mode' is used to use this function when choosing files for writting as well
     as for reading. When writting, warns if file exists. When reading,
     file must exist!!
    """
    
    if mode not in ("r", "w"):
        raise ValueError("wrong mode. Must be 'r' or 'w'")

    while 1:
        a = raw_input(prompt)
        
        path, fileName = os.path.split(a)
        #print path, fileName
        
        if path == "": path = os.getcwd()
        
        if not os.path.exists(path):
            print ("ERROR: directory does not exist. try again")
            continue    
    
        if os.path.isdir(a):
            print "ERROR: path denotes a directory. try again"
            continue
                
        if os.path.isfile(a) and mode == "w":
                overwrite =  readYN("file exists. Overwrite?")
                if not overwrite:
                    print "then try again"
                    continue
                    
        if not os.path.isfile(a) and mode == "r":
            print "file does not exist"
            continue
            
        return a                    
        
        # at this point, the directory exists, and the targetFile does not,
        # or the user want it to be rewritten
        break 
        
        
    return fileName
     
   
                




# ------------------ low level module operations ----------------------
        
"""
def write(module, address, value): #  write an address of a module
    global bus
    ser.write("SE %d %d %d %d\r" %(bus , module, address, value))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result
"""    
    
def read(address): #read an address of a module
    global bus
    #command = "
    ser.write("%i\r" %(address))
    time.sleep(delay)
    results =  ser.read(ser.inWaiting())       
    lines = results.split("\n")
    try:
       result = lines[1].split(" ")[-1]
    except:
        print "wrong module response format:"
        print "(command = " + command + ")"
        print "\n".join(lines)
        raise "error"     
    return result
    

#----------------------- high level module comms ---------------------------
"""    
def resetModule(module): #resets a module, using the RST command
    global bus
    moduleOn(module)
    command = "RST %d %d\r" % (bus, module)
    ser.write(command)
    time.sleep(delay*3)
    result =  ser.read(ser.inWaiting())
    print result

    	
def moduleOn(module): # Set a module On
    global bus
    ser.write("ON %d\r" % (bus))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    print result

"""
    
    
def readModule(): # reads and displays the parameters of the module (gain, threshold, pz, shap.)
    #moduleOn(module)
    print "  -------------------------------------"
    print "   module  values"
    print 
    for i in range(0,3, 1):
        gain  = read(i)
        if gain.isdigit():
            gainV = pow(1.22, int(gain))
            gainStr = "gain %s (x%6.3f)" % (gain, gainV)
        else:
            gainStr = "gain: [error]"
        print "  group %2i: " % (i + 1) + gainStr 
    print "  ----------------------------"
    for i in range(5,20, 1):
        threshold = read(i)
        if threshold.isdigit():
            volts = ((4.0 * int(threshold)) / 255.0)             # as stated in the mesytec STM-16 manual             
            rangePercent = (100 * volts) / 16
            thresholdStr = "threshold %s ,( %5.3fV, (%5.3f %% of range)" %(threshold, volts, rangePercent)
        else:
            thresholdStr = "threshold [error]"
            
        print "  channel %2i: " % (i - 4) + thresholdStr
    print "  ----------------------------"
    for i in range(22,38, 1):
        pz = read(i)
        if pz.isdigit():
            volts = ((4.0 * int(pz)) / 255.0)             # as stated in the mesytec STM-16 manual             
            rangePercent = (100 * volts) / 16
            pzStr = "pz %s ,( %5.3fV, (%5.3f %% of range)" %(pz, volts, rangePercent)
        else:
            pzStr = "Polo Zero [error]"
            
        print "  channel %2i: " % (i - 21) + pzStr
    print "  ----------------------------"

    for i in range(39,43, 1):
        shap  = read(i)
        if shap.isdigit():
	    		    
	    shapV = 2*int(gain)
	    if shapV==0: shapV=1
            shapStr = "shap %s (x%6.3f)" % (shap, shapV)
        else:
            shapStr = "gain: [error]"
        print "  group %2i: " % (i + 1) + shapStr 
    print "  ----------------------------"




"""

###########################################################################
def saveSettings(module, fileName):   # save all the settings of a module to a file
    values = [read(module, i) for i in range(0,44)]
    g = open(fileName, "w")
    g.write(" ".join(values))
    g.close()              
            

def loadSettings(module, fileName):   #   load a previously-saved settings of a module
    try:
        f = open(fileName, "r")
        s = f.read()
        f.close()
    except IOError:
        raise IOError("file does not exist")
        
                
    try:
        values = [int(i) for i in s.strip().split(" ")]
        
    except:
        raise IOError("Wrong file format: (expected space-separated values)")
    
    if len(values) != 44:
            raise IOError("Wrong file format: (expected 16 values)")
    
    for i in range(0, 44):
        write(module, i, values[i])
        

    

################################################################################## Interactive functions
def fnSaveSettings():  # interactive function to save settings
    module = readInteger("save which module on bus %d?" % bus)
    fileName = readFileName("name of the file?", "w")
    saveSettings(module, fileName)
    print "values saved."
    
    
def fnLoadSettings(): #interactive function to load settings

    
 
    fileName = readFileName("name of the file?", "r")
    module = readInteger("load into which module on bus %d?" % bus)
    loadSettings(module, fileName)
    
        
def fnModuleGain():  #interactive function to change globally the gain of a module 
 
    module = readInteger("  module?")
    gain = readInteger("  gain? (0-15)")
    setModuleGain(module, gain)
    readModule(module)

    
def fnModuleThreshold():  # interactive function to set globally the threshold of a module
    module = readInteger("  module?")
    v = readInteger("  threshold? (0-255)")
    setModuleThreshold(module, v)
    readModule(module)

    
def fnGain(): #interactive function to change the gain of a single channel in a module
    module = readInteger("  module?")
    channel = readInteger(" channel (1-16)?")
    gain = readInteger("  gain? (0-15)")
    moduleOn(module)
    write(module, (channel - 1) * 2, gain)


def fnThreshold(): #interactive function to change the thresholdof a single channel in a module
    module = readInteger("  module?")
    channel = readInteger(" channel (1-16)?")
    threshold = readInteger("  new threshold? (0-255)")
    moduleOn(module)
    write(module, 1 + (channel - 1) * 2, threshold)
    
    
def fnChangeBus(): # interactive function to change the bus
   global bus
   b = readInteger("  bus?")
   bus = b
   
   print "  active bus is now " + str(bus)
   

def fnSingleParameter(): #  interactive function to low-level change a channel of a module

    global bus
    m = readInteger("  module number?")
    a = readInteger("  address?")
    v = readInteger("  value?")
    moduleOn(m)
    write(m, a, v)
    print "  value of address %d in module %d on bus %d is now %d" % (a,m, bus, v)
    
    
def fnSaveAll(): # saves the configuration of all the modules
     fname = readFileName("file name?", "w")
    g = open(fname, "w")
    
    for module in range(12):
        print "saving module %d..." % module
        g.write("module %d\n" % module)
        for i in range(0, 32, 2):
            gain , threshold = read(module,i), read(module, i+1)
            g.write("%s %s\n" % (gain, threshold) )
    g.close()
                
      
def fnReadAll():  
    fname = readFileName("file name?", "r")
    g = open(fname, "r")
    
    for module in range(12):
        
        print "reading module %d"% module
        
        a = g.read(ser.inWaiting()).strip()
        if not a.startswith != "module":
           raise IOError (""file format error: expected "module" header "")
           
             
        
        
        for i in range(0,32, 2):
            gain , threshold = g.read(ser.inWaiting()).strip().split(" ")
            #print gain, threshold
            try:
                gain, threshold = int(gain), int(threshold)
            except:
                print gain, threshold
                raise IOError("format error in file")
                
            write(module, i, gain)
            write(module, i+1, threshold)
            
        
  """   
    
                    

################################################################################# Main Menu

def Menu():         # Main Menu
    global bus
    while 1:
        try:
	    #os.system('clear')            
	    print "*"*90
            print " a) SET RC ON        1) DISPLAY SETUP     6) SET BAUDRATE            p) SWITCH AUTO PZ    " 
            print " b) SET RC OFF       2) SET GAIN          7) SINGLE CHANNEL MODE     l) LOAD SETTINGS     "
            print " c) RESET SERIAL     3) SET THRESHOLD     8) SET MULTIP. BORDERS     s) SAVE SETTINGS     "
            print " d) COMMAND          4) SET POLO ZERO     9) SET MONITOR OUTPUT                           "
            print "                     5) SET SHAPING                                  x) EXIT              "                                                           
            print "*"*90
            option = raw_input(" OPTION ? :").lower().strip()
###################################################################### opciones a,b,c,d            
            if option == "a":
                 SetRC_On()
                 print "Remote Control is ON " 
            elif option == "b":
                 SetRC_Off()
                 print "Remote Control is OFF" 
            elif option == "c":
                closeSerial()
                time.sleep(2)
                openSerial()       
            elif option == "d":
                command = raw_input("command ?: ")
                ser.write(command)
                time.sleep(delay)
                r =  ser.read(ser.inWaiting())
                print "result: " + r
###################################################################### opciones p,l,s      
            elif option == "p":
                 AutoPZ()
                 #print "PZ automatic pz setting on/off" 
            elif option == "l":
                 module = readInteger("module? :" )
		 readModule(module)
                 #print "PZ automatic pz setting on/off" 
            elif option == "1":
                #address = raw_input("address ? :")
                #read(0)
                #ser.write("RE %i %i %i\r" %(bus, 21, 0))
                #ser.write("DS %d %d\r" %(bus, 21) )
                ser.write("DS\n")
		                
 		for line in ser.readlines():
  		   print line 
		#s=ser.readlines()
		print ""
		#print s
		#time.sleep(delay)
                result =  ser.read(ser.inWaiting())
                #result =  ser.read(ser.inWaiting())
                print result        
            elif option == "2":
                group = readInteger("group? (0:all, 1:Ch1-Ch4, 2:Ch5-Ch8, 3:Ch9-Ch12, 4:Ch13-Ch16)" )
                gain = readInteger("Gain? (0-15)" )
                SetGain(group,gain)
            elif option == "3":
                chan = readInteger("channel? (1-16, 17:all)" )
                thres = readInteger("Threshold? (0-255)" )
                SetThreshold(chan,thres)
            elif option == "4":
                chan = readInteger("channel? (1-16, 17:all)" )
                pz = readInteger("Polo Zero? (0-255)" )
                SetThreshold(chan,pz)
            elif option == "5":
                group = readInteger("group ? (0:all, 1:Ch1-Ch4, 2:Ch5-Ch8, 3:Ch9-Ch12, 4:Ch13-Ch16)" )
                shap = readInteger("Shap. Time ? (0-15)" )
                SetShaping(group,shap)
            elif option == "6":
                n = readInteger("Baudrate ? (1:9600 Bd. (default), 2: 19.200 Bd., 3: 28.400 Bd., 4: 57.600 Bd., 5: 115.200 Bd.)" )
                SetBaudrate(n)
            elif option == "7":
                high = readInteger("high ? (1-8)" )
                low  = readInteger("low ? (1-8)" )
                SetMult(high,low)
            elif option == "8":
                chan = readInteger("Channel ? (1-16)" )
                MonChan(chan)
            elif option == "9":
                mode = readInteger("mode ? (0 = off, 1 = on)" )     #elif option == "s":                 fnSaveSettings()
                SingleMode(mode)                                    #   elif option == "l":                 fnLoadSettings()
            elif option == "x":
                break
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

    bus = 0
    Introduction()

    try:
        openSerial()
    except:
        print "could not open serial port. Check that the device name "
        print "is correct (%s) and that the device is plugged to the connector" % DEVICE
        sys.exit(1) 
    
    Menu()
    closeSerial()
    
            
if __name__ == "__main__":   # does not execute main if this module was imported
    main()


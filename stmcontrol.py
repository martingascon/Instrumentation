#!/usr/bin/python
# Mesytec.py
#
# Simple control of Mesytec STM-16 modules
#
# == Author ==
#
# Angel Perea Martinez, Itto de Estructura de la materia, 2006
# Contact: aperea@iem.cfmac.csic.es
#
# == Known bugs ==
#
#
# == Impl. notes: ==
#
# * channels in a module go from 1 to 15 while addresses range from 0 to 32, so:
#    * gain is located in (channel - 1) * 2 
#    * threshold is in 1 + (channel - 1) * 2
#
# * bus is a global variable
#
# * a global variable 'delay' is used to prevent writting to fast into
#   the devices. its value was found experimentally
#
# * The read() method parses the answer of the module, which consists
#   on an echo + some data. it might exist a way to instruct the modules
#   to answer only with the data.
# 
#-----------------------------------------------------------------------


import sys
import time
import os
    
try:
    import serial # this assumes Pyserial and windows extensions installed
    
except Exception, e:
    print e
    print "ERROR: either win32 extension modules or pyserial do not seem to be installed"
    print "try to get them in "
    print "           http://pyserial.sourceforge.net "
    print "           http://www.python.net/crew/mhammond/ )"
    sys.exit(1)
    

#------- global data ---------

delay = 0.1
bus = 0

#------- RS232 Data ----------

BAUDS = 9600

#-------------------------------
# solve platform-dependent port names

if sys.platform == "win32":
    DEVICE = 'COM4'
    
elif sys.platform.startswith("linux"):
    DEVICE = '/dev/ttyS0'    # /dev/ttyUSB0
else:
    print "Warning: could not determine platform."
    print 'Please write the device name of the com1 port (windows = "com1", linux = "/dev/ttyS0")'
    DEVICE = raw_input("?")

print DEVICE



#-----------------------------

def banner():
    print "=================================="
    print "  mesytec STM-16 controller       "
    print "  v0.99 August-06                 "
    print " (aperea@iem.cfmac.csic.es)       "
    print "=================================="

    
def readYN(prompt):
    while 1:
       a = raw_input(prompt).lower().strip()
       if a == "y":
           return True
       elif a == "f":
           return False
           
def readInteger(prompt):
    """
    reads user input until the entry is a valid integer
    """
    while 1:
        a = raw_input(prompt)
        try:
            return int(a)
        except:
            print "  you should provide an integer"
            
    
def readFileName(prompt, mode):
    """
    gets a valid file name.
    
    'mode' is used to use this function when choosing files for writting aswell
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
     
   
                
#----------------- comms ----------------------------------

def openSerial():
    """
    opens the serial port
    """
    global ser
    print "opening serial port... (%s, %i bps)" % (DEVICE, BAUDS),
    ser = serial.Serial(DEVICE, BAUDS, timeout=2)        
    print "ok."
    
    
def closeSerial():
    """
    closes the port
    """
    global ser
    print "closing serial port...", 
    if ser != None and ser.isOpen():
        ser.close()
    print "ok."


# ------------------ low level module operations ----------------------
        
def moduleOn(module):
    """
    turns a module on
    """
    global bus
    ser.write("ON %i %i\r" % (bus, module))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    #print result
    

def moduleOff(module):
    """
    turns a module off
    """
    global bus
    ser.write("OFF %i %i\r" % (bus, module))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    #print result
      
    
def write(module, address, value):
    """
    write an address of a module
    """
    global bus
    ser.write("SE %i %i %i %i\r" %(bus , module, address, value))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result
    
    
def read(module, address):
    """
    read an address of a module
    """
    global bus
    command = "RE %i %i %i\r" % (bus, module, address)
    ser.write(command)
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
    
def resetModule(module):
    """
    resets a module, using the RST command
    """
    
    global bus
    moduleOn(module)
    command = "RST %i %i\r" % (bus, module)
    ser.write(command)
    time.sleep(delay*3)
    result =  ser.read(ser.inWaiting())
    print result

    	
def setModuleGain(module, gain):
    """
    sets the gain of the 16 channels of a module
    """
    moduleOn(module)
    for i in range(0, 32, 2):
        write(module, i, gain)

def setModuleThreshold(module, threshold):
    """
    sets the threshold of the 16  the channels of a module
    """
    moduleOn(module)
    for i in range(1, 33, 2):
        write(module, i, threshold)

    
    
def readModule(module):
    """
    reads and displays the parameters of the module
    """
    moduleOn(module)
    print "  ---------------------------"
    print "   module " + str(module) + " values"
    print 
    for i in range(0,32, 2):
        gain , threshold = read(module,i), read(module, i+1)
        
        if gain.isdigit():
            gainV = pow(1.22, int(gain))
            gainStr = "gain %s (x%6.3f)" % (gain, gainV)
        else:
            gainStr = "gain: [error]"
            
        if threshold.isdigit():
            volts = ((4.0 * int(threshold)) / 255.0)
                                   # as stated in the mesytec STM-16 manual             
            rangePercent = (100 * volts) / 16
            thresholdStr = "threshold %s ,( %5.3fV, (%5.3f %% of range)" %\
                                        (threshold, volts, rangePercent)
        else:
            thresholdStr = "threshold [error]"
            
        print "  channel %2i: " % (int(i / 2) + 1,) + gainStr + ", " + thresholdStr
        
    print "  ----------------------------"


def saveSettings(module, fileName):
    """
    save all the settings of a module to a file
    """
    
    values = [read(module, i) for i in range(0,32)]
    g = open(fileName, "w")
    g.write(" ".join(values))
    g.close()              
            

def loadSettings(module, fileName):
    """
    load a previously-saved settings of a module
    """
       
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
    
    if len(values) != 32:
            raise IOError("Wrong file format: (expected 16 values)")
    
    for i in range(0, 32):
        write(module, i, values[i])
        

        
                        
        
#---------------------------- Interactive functions ----------------------------

def fnSaveSettings():
    """
    interactive function to save settings
    """
    module = readInteger("save which module on bus %i?" % bus)
    fileName = readFileName("name of the file?", "w")
    saveSettings(module, fileName)
    print "values saved."
    
    
def fnLoadSettings():
    """
    interactive function to load settings
    """
    fileName = readFileName("name of the file?", "r")
    module = readInteger("load into which module on bus %i?" % bus)
    loadSettings(module, fileName)
    
        
def fnModuleGain():
    """
    interactive function to change globally the gain of a module    
    """
    module = readInteger("  module?")
    gain = readInteger("  gain? (0-15)")
    setModuleGain(module, gain)
    readModule(module)

    
def fnModuleThreshold():
    """
    interactive function to set globally the threshold of a module
    """
    module = readInteger("  module?")
    v = readInteger("  threshold? (0-255)")
    setModuleThreshold(module, v)
    readModule(module)

    
def fnGain():
    """
    interactive function to change the gain of a single channel in a module
    """
    module = readInteger("  module?")
    channel = readInteger(" channel (1-16)?")
    gain = readInteger("  gain? (0-15)")
    moduleOn(module)
    write(module, (channel - 1) * 2, gain)


def fnThreshold():
    """
    interactive function to change the thresholdof a single channel in a module
    """
    module = readInteger("  module?")
    channel = readInteger(" channel (1-16)?")
    threshold = readInteger("  new threshold? (0-255)")
    moduleOn(module)
    write(module, 1 + (channel - 1) * 2, threshold)
    
    
def fnChangeBus():
   """
   interactive function to change the bus
   """
   global bus
   print "  current Bus = " + str(bus)
   b = readInteger("  bus?")
   bus = b
   
   print "  active bus is now " + str(bus)
   

def fnSingleParameter():
    """
    interactive function to low-level change a channel of a module
    """
    global bus
    m = readInteger("  module number?")
    a = readInteger("  address?")
    v = readInteger("  value?")
    moduleOn(m)
    write(m, a, v)
    print "  value of address %i in module %i on bus %i is now %i" % (a,m, bus, v)
    
    
def fnSaveAll():
    """
    saves the configuration of all the modules
    """
    fname = readFileName("file name?", "w")
    g = open(fname, "w")
    
    for module in range(12):
        print "saving module %i..." % module
        g.write("module %i\n" % module)
        for i in range(0, 32, 2):
            gain , threshold = read(module,i), read(module, i+1)
            g.write("%s %s\n" % (gain, threshold) )
            
        
        
    g.close()
                
        
def fnReadAll():
    """
    """
    fname = readFileName("file name?", "r")
    g = open(fname, "r")
    
    for module in range(12):
        
        print "reading module %i"% module
        
        a = g.readline().strip()
        if not a.startswith != "module":
           raise IOError ("""file format error: expected "module" header """)
           
             
        
        
        for i in range(0,32, 2):
            gain , threshold = g.readline().strip().split(" ")
            #print gain, threshold
            try:
                gain, threshold = int(gain), int(threshold)
            except:
                print gain, threshold
                raise IOError("format error in file")
                
            write(module, i, gain)
            write(module, i+1, threshold)
            
        

    
                    
def interactiveMenu():
    """
    the application's main menu
    """
    global bus
    while 1:
        try:
            print
            print "-----------------------------------------------------------------------"
            print "  q) set _module_ gain              r) reset module                    "
            print "  w) set _module_ threshold         c) reset RS232 Connection          " 
            print "  g) set channel gain               +) set module on                   "
            print "  t) set channel threshold          -) set module off                  "
            print "  p) set individual parameter       d) direct command                  "
            print "  v) view module values             b) change bus                      "
            print "  l) load module settings                                              "
            print "  s) save module settings                                              "
            print "  a) save settings for all modules                                     "
            print "  z) load settings for all modules  x) exit                            "
            print "-----------------------------------------------------------------------" 
            print " Active bus " + str(bus)
            print "-----------------------------------------------------------------------"
            option = raw_input("option?").lower().strip()
            
            if option == "q":
                fnModuleGain()
                
            elif option == "w":
                fnModuleThreshold()
            
            if option == "g":
                fnGain()
                
            elif option == "t":
                fnThreshold()
                
            elif option == "p":
                fnSingleParameter()
            
            elif option == "v":
                m = readInteger("module?")
                readModule(m)
                
            elif option == "r":
                m = readInteger("module?")
                print "  resettingModule " + str(m) + "..."
                resetModule(m)
                time.sleep(1)
                
            elif option == "b":
                fnChangeBus()
                
            elif option == "c":
                closeSerial()
                time.sleep(2)
                openSerial()
            
            elif option == "a":
                fnSaveAll()
            
            elif option == "z":
                fnReadAll()
                
            elif option == "s":
                fnSaveSettings()
                
            elif option == "l":
                fnLoadSettings()
                
            elif option == "+":
                i = readInteger("module?")
                moduleOn(i)
                print "module " + str(i)  + " ON"
            
            elif option == "-":
                i = readInteger("module?")
                moduleOff(i)
                print "module " + str(i)  + " OFF"
            
            elif option == "d":
                command = raw_input("command?")
                ser.write(command)
                time.sleep(delay)
                r =  ser.read(ser.inWaiting())
                print "result: " + r
                
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
    """
    """
    bus = 0
    banner()
    
    try:
        openSerial()
    except:
        print "could not open serial port. Check that the device name "
        print "is correct (%s) and that the device is plugged to the connector" % DEVICE
        sys.exit(1)
        
    interactiveMenu()
    closeSerial()
    
            

if __name__ == "__main__":   # does not execute main if this module was imported
    main()


# -*- coding: utf-8 -*-
import os, sys, serial, time

BAUDS = 9600

bus = 0
delay = 0.2

#-------------------------------
# solve platform-dependent port names

if sys.platform == "win32":
    DEVICE = 'COM2'

elif sys.platform.startswith("linux"):
    DEVICE = '/dev/ttyUSB0'    # /dev/ttyUSB0
else:
    print "Warning: could not determine platform."
    print 'Please write the device name of the com1 port (windows = "com1", linux = "/dev/ttyS0")'
    DEVICE = raw_input("?")

#----------------------------------------------------------------------    
def readYN(prompt):
    while 1:
       a = raw_input(prompt).lower().strip()
       if a == "y":

           return True
       elif a == "f":
           return False
           

#----------------------------------------------------------------------    
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
            
    
#----------------------------------------------------------------------    
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
      
    
def write(module, address, value, testMode = False):
    """
    write an address of a module
    """
    global bus
    ser.write("SE %i %i %i %i\r" %(bus , module, address, value))
    time.sleep(delay)
    result =  ser.read(ser.inWaiting())
    return result
    
    
def read(module, address, testMode = False):
    """
    read an address of a module
    """
    global bus
    command = "RE %i %i %i\r" % (bus, module, address)
    ser.write(command)
    time.sleep(delay)
    results =  ser.read(ser.inWaiting())       
    lines = results.split("\n")
    #print lines
    try:
       result = lines[2].split(" ")[-1]
    except:
        print "wrong module response format:"
        print "(command = " + command + ")"
        print "\n".join(lines)
        raise "error"
        
    return result
    

#----------------------- high level module comms ---------------------------

def fnChangeBus(self):
      """
      interactive function to change the bus
      """
      global bus
      print "  current Bus = " + str(bus)
      b = readInteger("  bus?")
      bus = b
      
      print "  active bus is now " + str(bus)
    

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

        
  #----------------------- high level module comms ---------------------------

def fnChangeBus(self):
      """
      interactive function to change the bus
      """
      global bus
      print "  current Bus = " + str(bus)
      b = readInteger("  bus?")
      bus = b
        
      print "  active bus is now " + str(bus)



#===============================================
#
#===============================================
class DummyModule:
  """
  a dummy module to perform tests
  """

  def __init__(self):
    self.array = [0] * 100

  def set(channel, value):
    self.array[channel] =   value

  def get(channel, value):
    return self.array[channel]
      

#==============================================
#
#==============================================
class MesytecRC:

  def __init__(self):
    self.bus = 0

  
  def moduleOn(self, module):
      """
      turns a module on
      """
      ser.write("ON %i %i\r" % (self.bus, module))
      time.sleep(delay)
      result =  ser.read(ser.inWaiting())
      #print result
      

  def moduleOff(self, module):
      """
      turns a module off
      """
      ser.write("OFF %i %i\r" % (self.bus, module))
      time.sleep(delay)
      result =  ser.read(ser.inWaiting())
      #print result
        
      
  def write(self, module, address, value):
      """
      write an address of a module
      """
      ser.write("SE %i %i %i %i\r" % (self.bus , module, address, value) ) 
      time.sleep(delay)
      result =  ser.read(ser.inWaiting())
      return result
      
      
  def read(self, module, address):
      """
      read an address of a module
      """
      global bus
      command = "RE %i %i %i\r" % (self.bus, module, address)
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
      

  def changeBus(self, bus):
     self.bus = b


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

          

#==========================================
#
#==========================================
class DummyController:
  """
  dummy controller to test the program
  """

  def __init__(self):
    self.modules = [DummyModule(i) for i in range(16)]


  def moduleOn(self, module):
    pass


  def moduleOff(self, module):
    pass


  def write(self, module, address, value):
    self.modules[module].write(address, value)


  def read(self, module, address):
    return self.modules[module].read(address, value)


  def changeBus(self, bus):
    pass


  def resetModule(module):
    self.modules[modules].reset()



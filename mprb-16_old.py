#!/usr/bin/python
# -*- coding: utf-8 -*-
# Mesytec.py
#
# Simple control of Mesytec MSCF-16 modules
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
#
#
#
#
#-----------------------------------------------------------------------


import sys
import time
import os


from MesytecCommon import *

    
try:
    import serial # this assumes Pyserial and windows extensions installed
    
except Exception, e:
    print e
    print "ERROR: either win32 extension modules or pyserial does not seem to be installed"
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
    DEVICE = 'COM2'
    
elif sys.platform.startswith("linux"):
    DEVICE = '/dev/ttyUSB0'    # /dev/ttyUSB0
else:
    print "Warning: could not determine platform."
    print 'Please write the device name of the com1 port (windows = "com1", linux = "/dev/ttyS0")'
    DEVICE = raw_input("?")

print DEVICE



#-----------------------------


def banner():
    print "=================================="
    print "  mesytec MSCF-16 controller      "
    print "                                  "
    print " (aperea@iem.cfmac.csic.es)       "
    print "=================================="



#==================================================
#   MPRB_16
#=================================================
class MPRB_16:

    def __init__(self, address):
      """
      """
      self.address = address
      
    #----------------------------------
    def temperature(self):
      """
      """
      # 2048/70 + b = 25
      return (int(read(self.address, 18)) /  70) + (25 - 2048/70.0)
      
    #----------------------------------------------------------------------
    def printStatus(self):
      """
      reads and displays the parameters of the module
      """
      moduleOn(self.address)
      
      errorRegister = int(read(self.address, 21))
      errors = []
      a = str(bin(errorRegister))[2:]
      while len(a) < 16: a = "0" + a            
      for i in a:
        if i == "1":
          errors.append("ERROR")
        elif i == "0":
          errors.append("")
        else:
          raise
          
      
      print "----------------------------------------"
      
      for i in range(8):
        j = i + 8
        try:
          v1 = int(read(self.address, i)) / 10.0
        except:
          v1 = "no data"
          
        try:
          v2 = int(read(self.address, j)) / 10.0
        except:
          v2 = "no data"          
          
        print "  ch %2i: Voltage: %s V %s     ch %2i: Voltage: %s V   %s  " % (i, v1, errors[i], j, v2, errors[j])
        
      
      print
      print "  temperature %s " % (self.temperature())
      slope = int(read(self.address, 22))
      slope2 = (slope - 128) * (2.5 / 128)
      print " Temperature slope: %s (%4f V/ºC)" % (slope, slope2)
      print " Temperature offset: %s " % read(self.address, 23)
      print " Voltage limit: %s V" % (int(read(self.address, 25)) / 10.0)
      print " ch_error_flags: %s " % a      
      d = {"0": "frontpanel-controlled", "1": "high range, low sens.", "2": "low range, high sens."}
      print " Preamp range : %s " % d.get(read(self.address, 26), "nodata")
      print " Firmware revision: %s " % read(self.address, 31)   
      
      b = read(self.address, 24) 
      print " Bias %s applied " % {"0": "is NOT", "1": "IS"}.get(b, "no data (" + b + ")")
      print "----------------------------------------"
      
                               

    #----------------------------------------------------------------------
    def saveSettings(self, fileName):
      """
      save all the settings of a module to a file
      """
      
      values = [read(module, i) for i in range(0,32)]
      g = open(fileName, "w")
      g.write(" ".join(values))
      g.close()              
          
    #----------------------------------------------------------------------
    def loadSettings(self,  fileName):
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

    def fnSaveSettings(self):
      """
      interactive function to save settings
      """
      fileName = readFileName("name of the file?", "w")
      saveSettings(fileName)
      print "values saved."
      
    #----------------------------------------------------------------------
    def fnLoadSettings(self):
      """
      interactive function to load settings
      """
      fileName = readFileName("name of the file?", "r")
      loadSettings(fileName)
      


    #----------------------------------------------------------------------
    #          general
    #----------------------------------------------------------------------    
    def fnSetVLimit(self):
       
       while 1:
         v = readInteger("value? (0-6000) in tenths of volt")
         if v in range(0,6001): break
       write(self.address, 25, v)       

    #------------------------------------------------------------------
    def fnSetOffset(self):
       while 1:
         v = readInteger("value? (0-255)")
         if v in range(256): break

       write (self.address, 23, v)
         
    #------------------------------------------------------------------
    def fnSetSlope(self):
       
       while 1:
         v = readInteger("value? (0-255, 128 for 0 slope)")
         if v in range(256): break

       write(self.address, 22, v)       
       
    #------------------------------------------------------------------
    def fnSetVoltage(self):
       while 1:
         i = readInteger("channel (1-16)?") - 1
         if i in range(16): break

       while 1:
         v = readInteger("value? (0-255)")
         if v in range(256): break

       write(self.address, 22 + i, v)       
       

    #----------------------------------------------------------------------
    # fnSingleParameter
    #---------------------------------------------------------------------
    def fnSetRegister(self):
      """
      interactive function to low-level change a channel of a module
      """
      global bus
      a = readInteger("  address?")
      v = readInteger("  value?")
      moduleOn(self.address)
      write(self.address, a, v)
      print "  value of address %s in module %s on bus %s is now %s" % (a, self.address, bus, v)
    
    
    #------------------------------------
    def fnViewRegister(self):
      """
      interactive function to low-level change a channel of a module
      """
      global bus
      a = readInteger("  register?")      
      moduleOn(self.address)     
      v = read(self.address, a)
      print "  value of address %s in module %s on bus %s is '%s'" % (a,self.address, bus, v)
    
    #------------------------------------
    def fnSetVoltage(self):
      
      global bus
      while 1:
        a = readInteger("  channel?")            
        if a in range(16): break
        
      while 1:      
        v = readInteger("  value? (0-6000 in tenths of volt)")      
        if a in range(6001): break
        
      write(self.address, a, v)
      
    #------------------------------------
    def fnBiasOn(self):
      write(self.address, 24, 1)
    
    #------------------------------------
    def fnBiasOff(self):
      write(self.address, 24, 0)
    
    
    #----------------------------------------------------------------------            
    def interactiveMenu(self):
      """
      the application's main menu
      """
      global bus
      while 1:
        try:
          print 
          print 
          print "-------------------------------------------------------------------------"          
          print ""
          self.printStatus()          
          print "  s) set temperature slope                                               " 
          print "  v) set voltage                                                         "
          print "  o) set temperature offset                                              "
          print "  l) set voltage limit                                                   "
          print "  m) low-level register set                                              "
          print "  n) low-level register view                                              "
          print "  1) bias on                                             "
          print "  0) bias off"
          print "  x) exit                                                                "  
          print "-------------------------------------------------------------------------"
          option = raw_input("option?").lower().strip()
          
          fns = {
            "v": self.fnSetVoltage,
            "s": self.fnSetSlope,     "o": self.fnSetOffset,
            "l": self.fnSetVLimit,    "m": self.fnSetRegister, "n": self.fnViewRegister,
            "1": self.fnBiasOn,       "0": self.fnBiasOff,
          }
          
          if option == "x":
            break
          
          elif fns.has_key(option):
            fns[option]()
          
          else:
              print "wrong option"
              
          
        except KeyboardInterrupt:
          print
          print 
          print "<interrupted by user>"
          
        except:
          raise
          print "ERROR!"
   
   
#####################################################

def main():
    """
    """
    global bus
    bus = 0
    banner()
    
    try:
       openSerial()
    except:
        raise
        print "could not open serial port. Check that the device name "
        print "is correct (%s) and that the device is plugged to the connector" % DEVICE
        sys.exit(1)
    
    a = readInteger("MPRB address?")
    m = MPRB_16(a)
    m.interactiveMenu()
    closeSerial()
    
            

if __name__ == "__main__":   # does not execute main if this module was imported
    main()


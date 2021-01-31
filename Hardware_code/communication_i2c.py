import smbus
import time
bus = smbus.SMBus(1)
address = 0x04
def writeNumber(value):
 bus.write_byte(address, value)
 return -1
def readNumber():
 number = bus.read_byte(address)
 return number
while True:
  var=input("Enter 1/2 (1 for lock, 2 for unlock):")
  if not var:
     continue
  writeNumber(var)
  print "RPI: Hi Arduino, I sent you :", var
  # sleep one second
  time.sleep(1)
  number = readNumber()
  print "RPI: I received a digit(0 for empty, 1 for occupied): ", number, ""
  print "======================================\n"
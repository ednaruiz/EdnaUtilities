import numpy as np
import math 


def RightAscension():
  hours = float(raw_input("h: ")) 
  minutes = float(raw_input("m: ")) 
  seconds = float(raw_input("s: ")) 
  degrees = hours*(15) + minutes*(1/4.) + seconds*(1/240.)
  print(degrees) 
  
def DeclinationHAWC():  
  days = float(raw_input("d: ")) 
  minutes = float(raw_input("m: ")) 
  seconds = float(raw_input("s: ")) 
  degrees = hours*(1) + minutes*(1/60.) + seconds*(1/3600.)
  print(degrees) 
 
def DeclinationHESS():  
  days = float(raw_input("d: ")) 
  minutes = float(raw_input("m: ")) 
  seconds = float(raw_input("s: ")) 
  degrees = hours*(1) - minutes*(1/60.) - seconds*(1/3600.)
  print(degrees) 

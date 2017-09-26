import numpy as np
import math 


def RightAscension():
  hours = float(raw_input("h: ")) 
  minutes = float(raw_input("m: ")) 
  seconds = float(raw_input("s: ")) 
  degrees = hours*(15) + minutes*(1/4.) + seconds*(1/240.)
  print(degrees) 
  

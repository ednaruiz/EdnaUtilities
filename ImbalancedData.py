try:
  import numpy as np
  import pandas as pd
  from XCDF import XCDFFile
  from ROOT import *
except:
  print("Some modules were not found, desole")
  
  
class undersample:
  def __init__(self, data, column_name, bins):
    # we need to say bins, the column_name will be undersample to the content of the bin with less values.
    # bins should be as small as possible, yet, that makes it slower.
    if isinstance(data, pd.DataFrame)!:
      print("Data is not a pandas DataFrame!")
      break
    
    
    return under_data
  
  def plot_raw(self):
    # plot the raw input
  
  def plot_undersampled(self):
    

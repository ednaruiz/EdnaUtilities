try:
  import numpy as np
  import pandas as pd
  from XCDF import XCDFFile
  from ROOT import *
except:
  print("Some modules were not found, je suis tres desole")
  
  
class undersample:
  def __init__(self, data, column_name, bins):
    # we need to say bins, the column_name will be undersample to the content of the bin with less values.
    # bins should be as small as possible, yet, that makes it slower.
    if isinstance(data, pd.DataFrame)!:
      print("Data is not a pandas DataFrame!")
      break
    
    # i am very sorry this is going to be so raw and trivial,
    # i hope some day I can make it better
    
    maxv = max(data[column_name])
    minv = min(data[column_name])
    bining = np.linspace(maxv,minv,bins)
    counts = []
    for iBin in range (0,len(bining)-1):
      counts.append(len(data[column_name][data[column_name]>bining[iBin] and data[column_name]<bininb[iBin+1]]))
    limit = min(counts)
    print (limit)
    return under_data
  
  #def plot_raw(self):
    # plot the raw input
  
  #def plot_undersampled(self):
    

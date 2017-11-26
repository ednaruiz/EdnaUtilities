try:
  import numpy as np
  import pandas as pd
  from xcdf import XCDFFile
  from ROOT import *
  import matplotlib.pyplot as plt
except:
  print("Some modules were not found, je suis tres desole")
  

def read_xcdf(xcdf_file, fields,Fields):
  #if not isinstance(fields,list): 
  #  raise ValueError("Fields is not a list!")
  xf = XCDFFile(xcdf_file)
  nFields = len(Fields)
  lists = []
  for record in xf.fields(fields):
      lists.append(record)
   
  data = pd.DataFrame(data = lists, columns = Fields)
  return data
    
    
def undersample(data, column_name, bins):
  # we need to say bins, the column_name will be undersample to the content of the bin with less values.
  # bins should be as small as possible, yet, that makes it slower.
  if not isinstance(data, pd.DataFrame):
    raise ValueError("Data is not a pandas DataFrame!")


  # i am very sorry this is going to be so slow, raw and trivial,
  # i hope some day I can make it better
  print("here")
  maxv = max(data[column_name])
  minv = min(data[column_name])

  bining = np.linspace(minv,maxv,bins)
  print("here")
  counts = []
  for iBin in range (0,len(bining)-1):
    counts.append(len(data[column_name][data[column_name]>bining[iBin]][data[column_name]<bining[iBin+1]]))
  limit = min(counts)
  print(counts)
  under_data = pd.DataFrame(data=None, columns=data.columns)

  for iBin in range (0,len(bining)-1):
    ibb = pd.DataFrame(data[column_name][data[column_name]>bining[iBin]][data[column_name]<bining[iBin+1]][0:limit] , columns=data.columns)
    under_data = under_data.append(ibb,ignore_index=True)
  print("here")
  return under_data
  
  #def plot_raw(self):
    # plot the raw input
  
  #def plot_undersampled(self):
    
